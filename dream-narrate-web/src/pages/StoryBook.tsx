import { useState, useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2, SkipBack, SkipForward, Play, Pause, VolumeX, Award } from "lucide-react";

interface StoryPartData {
  story_part: string;
  question: string;
  options: string[];
  image_prompt: string;
}

interface StoryApiResponse {
  session_id?: number;
  one_line_plan?: string;
  story_part_data: StoryPartData;
  image_base64: string | null;
  audio_base64: string | null;
  part_number: number;
}

interface StoryHistoryItem {
  part: string;
  prompt: string;
}

interface QuizQuestion {
  question: string;
  options: string[];
  correct_answer: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

let audioContext: AudioContext | null = null;
try {
  if (typeof window !== "undefined") {
    audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  }
} catch (e) {
  console.error("Web Audio API not supported:", e);
}

const StoryBook = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // ── Story state ──────────────────────────────────────────────────────────
  const [oneLinePlan, setOneLinePlan] = useState<string | null>(null);
  const [currentPartData, setCurrentPartData] = useState<StoryPartData | null>(null);
  const [currentImage, setCurrentImage] = useState<string | null>(null);
  const [currentAudio, setCurrentAudio] = useState<string | null>(null);
  const [partNumber, setPartNumber] = useState<number>(0);
  const [storyHistory, setStoryHistory] = useState<StoryHistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState<string>("English");

  // ── Audio state ───────────────────────────────────────────────────────────
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [isAudioPaused, setIsAudioPaused] = useState(false);
  // audioCurrentTime is stored in a ref so seekAudio always reads the latest
  // value without depending on React's async state flush.
  const audioCurrentTimeRef = useRef<number>(0);
  const currentAudioSource = useRef<AudioBufferSourceNode | null>(null);
  const audioStartTimeRef = useRef<number>(0); // audioContext.currentTime when playback started
  const decodedAudioBuffer = useRef<AudioBuffer | null>(null);
  const hasPlayedOnce = useRef<boolean>(false); // track first play for replay counting

  // ── Tracking state ────────────────────────────────────────────────────────
  const [sessionId, setSessionId] = useState<number | null>(null);
  const sessionStartTime = useRef<number>(Date.now());
  const [audioReplayCount, setAudioReplayCount] = useState<number>(0);

  // ── Quiz / completion state ───────────────────────────────────────────────
  const [isComplete, setIsComplete] = useState(false);
  const [isQuizLoading, setIsQuizLoading] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);
  const [quizQuestions, setQuizQuestions] = useState<QuizQuestion[]>([]);
  const [quizAnswers, setQuizAnswers] = useState<Record<number, string>>({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState<number>(0);

  // ── Initialise story from navigation state ────────────────────────────────
  useEffect(() => {
    const initialState = location.state?.initialStoryData as StoryApiResponse | undefined;
    const initialLanguage = location.state?.language as string | undefined;

    if (initialState?.story_part_data) {
      setSessionId(initialState.session_id ?? null);
      setOneLinePlan(initialState.one_line_plan ?? null);
      setCurrentPartData(initialState.story_part_data);
      setCurrentImage(initialState.image_base64);
      setCurrentAudio(initialState.audio_base64);
      setPartNumber(initialState.part_number);
      setStoryHistory([]);
      sessionStartTime.current = Date.now();
      if (initialLanguage) setLanguage(initialLanguage);
    } else {
      navigate("/dashboard");
    }

    return () => stopAudio();
  }, [location.state, navigate]);

  // Reset audio buffer every time a new story part loads
  useEffect(() => {
    stopAudio();
    decodedAudioBuffer.current = null;
    audioCurrentTimeRef.current = 0;
    hasPlayedOnce.current = false;
  }, [currentPartData]);

  // ── Tracking helpers ──────────────────────────────────────────────────────
  const trackButtonClick = async (buttonType: string) => {
    if (!sessionId) return;
    try {
      await fetch(`${API_BASE_URL}/api/tracking/button-click`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, button_type: buttonType, part_number: partNumber }),
      });
    } catch (_) {}
  };

  const trackAudioReplay = async () => {
    setAudioReplayCount((c) => c + 1);
    if (!sessionId) return;
    try {
      await fetch(`${API_BASE_URL}/api/tracking/audio-replay`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, part_number: partNumber }),
      });
    } catch (_) {}
  };

  // ── Audio controls ────────────────────────────────────────────────────────
  const stopAudio = () => {
    if (currentAudioSource.current) {
      try {
        currentAudioSource.current.stop();
        currentAudioSource.current.disconnect();
      } catch (_) {}
      currentAudioSource.current = null;
    }
    setIsAudioPlaying(false);
    setIsAudioPaused(false);
  };

  /**
   * Play (or resume) audio from a given position.
   * @param startFrom  seconds offset to start from. Uses audioCurrentTimeRef when omitted.
   * @param isReplay   whether to record this as a replay event.
   */
  const playAudio = async (startFrom?: number, isReplay = false) => {
    if (!currentAudio || !audioContext) return;

    // Resume suspended context (browsers block audio until user gesture)
    if (audioContext.state === "suspended") {
      await audioContext.resume();
    }

    if (isReplay) await trackAudioReplay();

    stopAudio();

    try {
      // Decode once and cache
      if (!decodedAudioBuffer.current) {
        console.log("🔄 Decoding audio...");
        const binary = window.atob(currentAudio);
        const bytes = new Uint8Array(binary.length);
        for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
        decodedAudioBuffer.current = await audioContext.decodeAudioData(bytes.buffer);
        console.log("✅ Decoded, duration:", decodedAudioBuffer.current.duration.toFixed(2), "s");
      }

      const buffer = decodedAudioBuffer.current;
      const offset = Math.min(
        startFrom !== undefined ? startFrom : audioCurrentTimeRef.current,
        buffer.duration - 0.1
      );

      console.log("▶️ Play from", offset.toFixed(2), "s");

      const source = audioContext.createBufferSource();
      source.buffer = buffer;
      source.connect(audioContext.destination);
      currentAudioSource.current = source;
      // Record context time so we can compute elapsed later
      audioStartTimeRef.current = audioContext.currentTime - offset;

      source.onended = () => {
        // Guard: only reset state for the source that is still active.
        // When seekAudio stops an old source and starts a new one, the old
        // source's onended fires asynchronously and must NOT overwrite the new
        // source's position (which would silently reset rewind to 0).
        if (currentAudioSource.current === source) {
          console.log("🏁 Audio ended naturally");
          setIsAudioPlaying(false);
          setIsAudioPaused(false);
          audioCurrentTimeRef.current = 0;
          currentAudioSource.current = null;
        } else {
          console.log("🔁 Old source ended after seek — ignoring");
        }
      };

      source.start(0, offset);
      setIsAudioPlaying(true);
      setIsAudioPaused(false);

      await trackButtonClick(isReplay ? "audio_replay" : "audio_play");
    } catch (err) {
      console.error("❌ Audio error:", err);
      setIsAudioPlaying(false);
      currentAudioSource.current = null;
    }
  };

  const pauseAudio = () => {
    if (!currentAudioSource.current || !audioContext) return;
    // Capture elapsed time before stopping
    const elapsed = audioContext.currentTime - audioStartTimeRef.current;
    console.log("⏸️ Pausing at", elapsed.toFixed(2), "s");
    audioCurrentTimeRef.current = elapsed;
    stopAudio();
    setIsAudioPaused(true);
    trackButtonClick("audio_pause");
  };

  /**
   * Seek by `seconds` relative to current position.
   * Works whether audio is playing, paused, or stopped.
   * FIX: computes new position into a local variable and passes it directly
   * to playAudio — avoids the stale-state bug that killed seek after first use.
   */
  const seekAudio = async (seconds: number) => {
    if (!audioContext || !decodedAudioBuffer.current) {
      console.log("❌ Seek blocked: no buffer yet. Play audio first.");
      return;
    }

    const wasPlaying = isAudioPlaying;
    const buffer = decodedAudioBuffer.current;

    // Snapshot current position from ref (always fresh, no closure staleness)
    const currentPos = wasPlaying
      ? audioContext.currentTime - audioStartTimeRef.current
      : audioCurrentTimeRef.current;

    const newTime = Math.max(0, Math.min(currentPos + seconds, buffer.duration - 0.5));
    console.log(`⏩ Seek ${seconds > 0 ? "+" : ""}${seconds}s : ${currentPos.toFixed(2)} → ${newTime.toFixed(2)}`);

    if (wasPlaying) stopAudio();

    // Store new position in ref immediately (no async state flush needed)
    audioCurrentTimeRef.current = newTime;

    if (wasPlaying) {
      // Pass newTime directly — bypasses stale state entirely
      await playAudio(newTime, false);
    }

    await trackButtonClick(seconds > 0 ? "audio_forward" : "audio_rewind");
  };

  // ── Story progression ─────────────────────────────────────────────────────
  const handleChoice = async (choiceText: string, choiceIndex: number) => {
    if (isLoading || !currentPartData || !oneLinePlan) return;

    await trackButtonClick(`choice_${choiceIndex}`);
    stopAudio();
    setIsLoading(true);

    const historyUpdate: StoryHistoryItem = {
      part: currentPartData.story_part,
      prompt: currentPartData.image_prompt,
    };
    const nextHistory = [...storyHistory, historyUpdate];

    try {
      const response = await fetch(`${API_BASE_URL}/continue-story`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          one_line_plan: oneLinePlan,
          story_context_history: nextHistory,
          child_choice: choiceText,
          part_number: partNumber,
          language: language,
          art_style_guide: "A simple, friendly, and colorful children's book illustration...",
        }),
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const nextPartData = (await response.json()) as StoryApiResponse;

      console.log("📦 Part", nextPartData.part_number, "received");
      console.log("  question:", nextPartData.story_part_data?.question || "none");
      console.log("  options:", nextPartData.story_part_data?.options || "none");

      if (!nextPartData?.story_part_data) throw new Error("Invalid story data from server.");

      setCurrentPartData(nextPartData.story_part_data);
      setCurrentImage(nextPartData.image_base64);
      setCurrentAudio(nextPartData.audio_base64);
      setPartNumber(nextPartData.part_number);
      setStoryHistory(nextHistory);
      audioCurrentTimeRef.current = 0;

      // Part 5 is the final part — we show it normally, then a "Continue to Quiz" button.
      // Do NOT set isComplete here; that happens when the user taps "Continue to Quiz".
    } catch (err) {
      console.error("Error continuing story:", err);
      alert(`Could not continue. ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsLoading(false);
    }
  };

  // ── Session & quiz ────────────────────────────────────────────────────────
  const endSession = async () => {
    if (!sessionId) return;
    const duration = Math.floor((Date.now() - sessionStartTime.current) / 1000);
    try {
      await fetch(`${API_BASE_URL}/api/session/${sessionId}/end`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, duration_seconds: duration }),
      });
    } catch (_) {}
  };

  /**
   * Generate quiz. Accepts pre-built story summary to avoid stale state.
   */
  const generateQuiz = async (storySummary: string) => {
    try {
      // 45-second timeout — quiz generation can be slow but shouldn't hang forever
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 45000);

      let response: Response;
      try {
        response = await fetch(`${API_BASE_URL}/api/quiz/generate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ story_summary: storySummary, educational_theme: "learning and growth" }),
          signal: controller.signal,
        });
      } finally {
        clearTimeout(timeoutId);
      }
      if (response.ok) {
        const data = await response.json();

        // Log the raw payload so we can see exact field names Gemini used
        console.log("🔍 Raw quiz payload:", JSON.stringify(data, null, 2));

        const raw: any[] = Array.isArray(data.quiz) ? data.quiz : [];
        console.log("📝 Raw count:", raw.length);
        if (raw.length > 0) console.log("📝 First question keys:", Object.keys(raw[0]));

        // Normalize: handle field-name variations Gemini might use (options/Options/choices etc.)
        const valid: QuizQuestion[] = raw
          .map((q: any) => ({
            question: q.question ?? q.Question ?? "",
            options: Array.isArray(q.options) ? q.options
                   : Array.isArray(q.Options) ? q.Options
                   : Array.isArray(q.choices) ? q.choices : [],
            correct_answer: q.correct_answer ?? q.correctAnswer ?? q.CorrectAnswer ?? q.answer ?? "",
          }))
          .filter((q) => q.question.length > 0 && q.options.length > 0);

        console.log("📝 Valid after normalize:", valid.length, valid);
        setQuizQuestions(valid);
      } else {
        console.error("Quiz API error:", response.status);
        setQuizQuestions([]); // fallback: empty = show skip option
      }
    } catch (err) {
      console.error("Quiz fetch error:", err);
      setQuizQuestions([]);
    }
    setShowQuiz(true);
  };

  /**
   * Called when user taps "Continue to Quiz" on part 5.
   * Builds story summary from live local variables (not stale state) to avoid
   * passing an empty summary to the quiz API.
   */
  const handleContinueToQuiz = async () => {
    // IMPORTANT: update state BEFORE any await so React re-renders immediately,
    // hiding the button and preventing duplicate clicks from queuing up.
    stopAudio();
    setIsComplete(true);
    setIsQuizLoading(true);

    // Build summary synchronously from current captured variables before any await
    const parts = [...storyHistory.map((h) => h.part)];
    if (currentPartData?.story_part) parts.push(currentPartData.story_part);
    const summary = parts.join(" ");
    console.log("📖 Story summary length:", summary.length, "chars");

    // All awaits come after the state updates above
    await trackButtonClick("continue_to_quiz");
    await endSession();
    await generateQuiz(summary);
    setIsQuizLoading(false);
  };

  const submitQuiz = async () => {
    if (!sessionId) {
      // No session — just show score locally
      const score = quizQuestions.filter((q, i) => quizAnswers[i] === q.correct_answer).length;
      setQuizScore(score);
      setQuizSubmitted(true);
      return;
    }
    const answers = quizQuestions.map((q, i) => ({
      question: q.question,
      correct_answer: q.correct_answer,
      user_answer: quizAnswers[i] || "",
    }));
    try {
      const res = await fetch(`${API_BASE_URL}/api/quiz/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, answers }),
      });
      if (res.ok) {
        const result = await res.json();
        setQuizScore(result.score);
      } else {
        const score = answers.filter((a) => a.user_answer === a.correct_answer).length;
        setQuizScore(score);
      }
    } catch (_) {
      const score = answers.filter((a) => a.user_answer === a.correct_answer).length;
      setQuizScore(score);
    }
    setQuizSubmitted(true);
    await trackButtonClick("quiz_submitted");
  };

  const downloadReport = async () => {
    if (!sessionId) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/session/${sessionId}/report`);
      if (res.ok) {
        const data = await res.json();
        const blob = new Blob([JSON.stringify(data.report, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `story_report_${sessionId}.json`;
        a.click();
        URL.revokeObjectURL(url);
        await trackButtonClick("download_report");
      }
    } catch (_) {}
  };

  // ── Early guards ──────────────────────────────────────────────────────────
  if (!currentPartData) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  // ── Quiz loading screen ───────────────────────────────────────────────────
  if (isComplete && isQuizLoading) {
    return (
      <div className="flex flex-col justify-center items-center min-h-screen gap-4">
        <Loader2 className="w-12 h-12 animate-spin text-primary" />
        <p className="text-lg text-muted-foreground">Preparing your quiz…</p>
      </div>
    );
  }

  // ── Quiz screen ───────────────────────────────────────────────────────────
  if (isComplete && showQuiz && !quizSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-6 md:p-12">
        <Card className="max-w-3xl mx-auto">
          <CardHeader>
            <CardTitle className="text-3xl text-center">📚 Story Quiz!</CardTitle>
          </CardHeader>
          <CardContent>
            {quizQuestions.length === 0 ? (
              // Fallback when quiz generation failed or returned empty
              <div className="text-center space-y-4 py-8">
                <p className="text-muted-foreground">Quiz unavailable right now.</p>
                <Button onClick={() => setQuizSubmitted(true)}>See Your Report →</Button>
              </div>
            ) : (
              <div className="space-y-6">
                {quizQuestions.map((q, idx) => (
                  <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                    <p className="font-semibold mb-3">
                      {idx + 1}. {q.question}
                    </p>
                    <div className="space-y-2">
                      {(q.options ?? []).map((option, optIdx) => (
                        <Button
                          key={optIdx}
                          variant={quizAnswers[idx] === option ? "default" : "outline"}
                          className="w-full justify-start"
                          onClick={() => setQuizAnswers({ ...quizAnswers, [idx]: option })}
                        >
                          {option}
                        </Button>
                      ))}
                    </div>
                  </div>
                ))}
                <Button
                  onClick={submitQuiz}
                  className="w-full"
                  disabled={Object.keys(quizAnswers).length !== quizQuestions.length}
                >
                  Submit Quiz
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    );
  }

  // ── Results screen ────────────────────────────────────────────────────────
  if (isComplete && quizSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 p-8 flex items-center justify-center">
        <Card className="max-w-2xl w-full">
          <CardContent className="p-12 text-center space-y-6">
            <Award className="w-24 h-24 mx-auto text-yellow-500" />
            <h2 className="text-4xl font-bold">Great Job!</h2>
            <p className="text-2xl">
              You scored {quizScore} out of {quizQuestions.length}!
            </p>
            <p className="text-muted-foreground">Audio replays this session: {audioReplayCount}</p>
            <div className="flex gap-4 justify-center pt-4 flex-wrap">
              <Button onClick={downloadReport} variant="outline">
                Download Report
              </Button>
              <Button onClick={() => navigate("/dashboard")}>Start New Story</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // ── Main story view ───────────────────────────────────────────────────────
  const isFinalPart = partNumber === 5;

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 flex items-center justify-center p-4 md:p-8">
      <div className="max-w-7xl w-full">
        {/* Replay counter */}
        <div className="text-center mb-4 text-sm text-gray-500">
          Audio Replays: {audioReplayCount}
        </div>

        <div className="grid md:grid-cols-2 gap-0 bg-white rounded-2xl shadow-2xl md:overflow-hidden md:min-h-[60vh] md:max-h-[85vh]">
          {/* Left — illustration */}
          <div className="bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center p-3 md:p-12">
            {currentImage ? (
              <img
                src={`data:image/jpeg;base64,${currentImage}`}
                alt={`Story illustration part ${partNumber}`}
                className="w-full object-contain rounded-lg max-h-[35vh] md:max-h-[70vh]"
              />
            ) : (
              <div className="w-full h-full bg-muted rounded-lg flex items-center justify-center">
                <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
              </div>
            )}
          </div>

          {/* Right — text & controls */}
          <div className="bg-amber-50/30 p-6 md:p-12 flex flex-col overflow-y-auto max-h-[85vh]">
            <div className="flex-1 mb-4">
              {/* Audio controls — only when audio is available */}
              {currentAudio && audioContext && (
                <div className="mb-4 flex items-center gap-2 justify-end">
                  <Button
                    variant="ghost"
                    size="icon"
                    title="Rewind 10 s"
                    onClick={() => seekAudio(-10)}
                  >
                    <SkipBack className="w-5 h-5" />
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    title={isAudioPlaying ? "Pause" : "Play"}
                    onClick={() => {
                      if (isAudioPlaying) {
                        pauseAudio();
                      } else {
                        // If paused mid-way, resume. Otherwise play fresh.
                        const isReplay = hasPlayedOnce.current;
                        hasPlayedOnce.current = true;
                        playAudio(audioCurrentTimeRef.current, isReplay);
                      }
                    }}
                  >
                    {isAudioPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    title="Forward 10 s"
                    onClick={() => seekAudio(10)}
                  >
                    <SkipForward className="w-5 h-5" />
                  </Button>

                  <Button
                    variant="ghost"
                    size="icon"
                    title="Stop"
                    onClick={() => {
                      stopAudio();
                      audioCurrentTimeRef.current = 0;
                    }}
                  >
                    <VolumeX className="w-5 h-5" />
                  </Button>
                </div>
              )}

              {/* Story text */}
              <p className="text-lg md:text-xl leading-relaxed font-serif mb-6">
                {currentPartData.story_part}
              </p>

              {/* Question — shown only for parts 1-4 */}
              {currentPartData.question && !isFinalPart && (
                <p className="text-base md:text-lg font-serif italic text-gray-600 mb-6">
                  {currentPartData.question}
                </p>
              )}
            </div>

            {/* Bottom action area */}
            <div className="space-y-3 mt-auto pt-4">
              {isLoading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="w-8 h-8 animate-spin" />
                  <p className="ml-3 text-muted-foreground">Generating next part…</p>
                </div>
              ) : isFinalPart ? (
                // Part 5 — story is over, offer the quiz
                <div className="text-center space-y-3">
                  <p className="text-sm text-muted-foreground italic">The story has ended!</p>
                  <Button
                    onClick={handleContinueToQuiz}
                    disabled={isComplete || isLoading}
                    size="lg"
                    className="w-full rounded-full py-6 text-lg bg-gradient-to-r from-primary to-secondary text-primary-foreground shadow-lg hover:shadow-xl disabled:opacity-50"
                  >
                    Continue to Quiz →
                  </Button>
                </div>
              ) : (
                // Parts 1-4 — show choice buttons
                currentPartData.options.map((option, index) => (
                  <Button
                    key={index}
                    onClick={() => handleChoice(option, index)}
                    variant="outline"
                    className="w-full justify-start rounded-full py-6 px-6 text-base font-semibold"
                    disabled={isLoading}
                  >
                    {option}
                  </Button>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StoryBook;
