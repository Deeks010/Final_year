// import { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { Button } from "@/components/ui/button";
// import { Input } from "@/components/ui/input";
// import { Label } from "@/components/ui/label";
// import { Textarea } from "@/components/ui/textarea";
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
// import { Card, CardContent } from "@/components/ui/card";
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
// const Onboarding = () => {
//   const navigate = useNavigate();
//   const [step, setStep] = useState(1);
//   const [childName, setChildName] = useState("");
//   const [childAge, setChildAge] = useState("");
//   const [interests, setInterests] = useState("");
//   const [favoriteActivities, setFavoriteActivities] = useState("");
//   const [autismSeverity, setAutismSeverity] = useState("");
//   const [communicationLevel, setCommunicationLevel] = useState("");
//   const [isLoading, setIsLoading] = useState(false); // Add a loading state

//   const handleFinish = () => {
//     // Store data in localStorage for dashboard
//     localStorage.setItem(
//       "childProfile",
//       JSON.stringify({
//         name: childName,
//         age: childAge,
//         interests,
//         favoriteActivities,
//         autismSeverity,
//         communicationLevel,
//       })
//     );
//     navigate("/dashboard");
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center p-4">
//       <Card className="w-full max-w-2xl shadow-lg">
//         <CardContent className="p-8">
//           <div className="mb-8 text-center">
//             <p className="text-sm text-muted-foreground font-semibold">
//               Step {step} of 3
//             </p>
//           </div>

//           {step === 1 && (
//             <div className="space-y-6">
//               <h1 className="text-3xl font-bold text-center text-foreground mb-2">
//                 Tell us about your reader!
//               </h1>

//               <div className="space-y-4">
//                 <div className="space-y-2">
//                   <Label htmlFor="childName">Child's Name</Label>
//                   <Input
//                     id="childName"
//                     placeholder="e.g., Leo"
//                     value={childName}
//                     onChange={(e) => setChildName(e.target.value)}
//                     className="text-lg"
//                   />
//                 </div>

//                 <div className="space-y-2">
//                   <Label htmlFor="childAge">Child's Age</Label>
//                   <Input
//                     id="childAge"
//                     type="number"
//                     placeholder="e.g., 6"
//                     value={childAge}
//                     onChange={(e) => setChildAge(e.target.value)}
//                     className="text-lg"
//                   />
//                 </div>
//               </div>

//               <Button
//                 onClick={() => setStep(2)}
//                 disabled={!childName || !childAge}
//                 className="w-full rounded-full py-6 text-lg"
//                 size="lg"
//               >
//                 Next
//               </Button>
//             </div>
//           )}

//           {step === 2 && (
//             <div className="space-y-6">
//               <h1 className="text-3xl font-bold text-center text-foreground mb-2">
//                 Tell us about their interests
//               </h1>

//               <div className="space-y-4">
//                 <div className="space-y-2">
//                   <Label htmlFor="interests">Interests & Preferences</Label>
//                   <Textarea
//                     id="interests"
//                     placeholder="Describe the child's interests, favorite topics, things they enjoy..."
//                     value={interests}
//                     onChange={(e) => setInterests(e.target.value)}
//                     className="min-h-[120px] text-base"
//                   />
//                 </div>

//                 <div className="space-y-2">
//                   <Label htmlFor="favoriteActivities">Favorite Activities</Label>
//                   <Textarea
//                     id="favoriteActivities"
//                     placeholder="Specific activities the child enjoys..."
//                     value={favoriteActivities}
//                     onChange={(e) => setFavoriteActivities(e.target.value)}
//                     className="min-h-[120px] text-base"
//                   />
//                 </div>
//               </div>

//               <div className="flex gap-3">
//                 <Button
//                   onClick={() => setStep(1)}
//                   variant="outline"
//                   className="flex-1 rounded-full py-6 text-lg"
//                   size="lg"
//                 >
//                   Back
//                 </Button>
//                 <Button
//                   onClick={() => setStep(3)}
//                   disabled={!interests || !favoriteActivities}
//                   className="flex-1 rounded-full py-6 text-lg"
//                   size="lg"
//                 >
//                   Next
//                 </Button>
//               </div>
//             </div>
//           )}

//           {step === 3 && (
//             <div className="space-y-6">
//               <h1 className="text-3xl font-bold text-center text-foreground mb-6">
//                 Child Assessment
//               </h1>

//               <div className="space-y-4">
//                 <div className="space-y-2">
//                   <Label htmlFor="autismSeverity">Autism Severity</Label>
//                   <Select value={autismSeverity} onValueChange={setAutismSeverity}>
//                     <SelectTrigger id="autismSeverity" className="text-base">
//                       <SelectValue placeholder="Select..." />
//                     </SelectTrigger>
//                     <SelectContent>
//                       <SelectItem value="mild">Mild</SelectItem>
//                       <SelectItem value="moderate">Moderate</SelectItem>
//                       <SelectItem value="severe">Severe</SelectItem>
//                     </SelectContent>
//                   </Select>
//                 </div>

//                 <div className="space-y-2">
//                   <Label htmlFor="communicationLevel">Communication Level</Label>
//                   <Select value={communicationLevel} onValueChange={setCommunicationLevel}>
//                     <SelectTrigger id="communicationLevel" className="text-base">
//                       <SelectValue placeholder="Select..." />
//                     </SelectTrigger>
//                     <SelectContent>
//                       <SelectItem value="verbal">Verbal</SelectItem>
//                       <SelectItem value="limited">Limited</SelectItem>
//                       <SelectItem value="non-verbal">Non-verbal</SelectItem>
//                     </SelectContent>
//                   </Select>
//                 </div>
//               </div>

//               <div className="flex gap-3 pt-4">
//                 <Button
//                   onClick={() => setStep(2)}
//                   variant="outline"
//                   className="flex-1 rounded-full py-6 text-lg"
//                   size="lg"
//                 >
//                   Back
//                 </Button>
//                 <Button
//                   onClick={handleFinish}
//                   disabled={!autismSeverity || !communicationLevel}
//                   className="flex-1 rounded-full py-6 text-lg bg-secondary hover:bg-secondary/90"
//                   size="lg"
//                 >
//                   Finish Setup!
//                 </Button>
//               </div>
//             </div>
//           )}
//         </CardContent>
//       </Card>
//     </div>
//   );
// };

// export default Onboarding;


import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2 } from "lucide-react"; // --- NEW: Import loader icon

// --- NEW: Define API Base URL (Make sure VITE_API_BASE_URL is in your .env file) ---
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

const Onboarding = () => {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [childName, setChildName] = useState("");
  const [childAge, setChildAge] = useState("");
  const [interests, setInterests] = useState("");
  const [favoriteActivities, setFavoriteActivities] = useState("");
  const [autismSeverity, setAutismSeverity] = useState("");
  const [communicationLevel, setCommunicationLevel] = useState("");
  const [isLoading, setIsLoading] = useState(false); // --- NEW: State for loading indicator ---

  // --- MODIFIED: This function now calls the backend API ---
  const handleFinish = async () => {
    setIsLoading(true); // Start loading

    // The backend expects age to be an integer
    const ageAsNumber = parseInt(childAge, 10);
    if (isNaN(ageAsNumber)) {
        alert("Please enter a valid age.");
        setIsLoading(false);
        return;
    }

    const profileData = {
      name: childName,
      age: ageAsNumber,
      interests: interests,
      favoriteActivities: favoriteActivities,
      autismSeverity: autismSeverity,
      communicationLevel: communicationLevel,
    };

    try {
      const response = await fetch(`${API_BASE_URL}/onboard`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        // Try to get a detailed error message from the backend
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to save the profile. Please try again.');
      }

      // --- REMOVED: No longer saving full profile to localStorage ---
      // localStorage.setItem("childProfile", JSON.stringify(...));
      
      // --- NEW: We can set a simple flag to remember onboarding is done ---
      localStorage.setItem("onboardingComplete", "true");

      console.log("Onboarding successful, navigating to dashboard.");
      navigate("/dashboard");

    } catch (error) {
      console.error("Onboarding failed:", error);
      alert(`Could not save profile. Please check the backend and try again. Error: ${error instanceof Error ? error.message : "Unknown error"}`);
    } finally {
        setIsLoading(false); // Stop loading, regardless of outcome
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-lg">
        <CardContent className="p-8">
          <div className="mb-8 text-center">
            <p className="text-sm text-muted-foreground font-semibold">
              Step {step} of 3
            </p>
          </div>

          {step === 1 && (
            <div className="space-y-6">
              <h1 className="text-3xl font-bold text-center text-foreground mb-2">
                Tell us about your reader!
              </h1>

              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="childName">Child's Name</Label>
                  <Input
                    id="childName"
                    placeholder="e.g., Leo"
                    value={childName}
                    onChange={(e) => setChildName(e.target.value)}
                    className="text-lg"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="childAge">Child's Age</Label>
                  <Input
                    id="childAge"
                    type="number"
                    placeholder="e.g., 6"
                    value={childAge}
                    onChange={(e) => setChildAge(e.target.value)}
                    className="text-lg"
                  />
                </div>
              </div>

              <Button
                onClick={() => setStep(2)}
                disabled={!childName || !childAge}
                className="w-full rounded-full py-6 text-lg"
                size="lg"
              >
                Next
              </Button>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <h1 className="text-3xl font-bold text-center text-foreground mb-2">
                Tell us about their interests
              </h1>

              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="interests">Interests & Preferences</Label>
                  <Textarea
                    id="interests"
                    placeholder="Describe the child's interests, favorite topics, things they enjoy..."
                    value={interests}
                    onChange={(e) => setInterests(e.target.value)}
                    className="min-h-[120px] text-base"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="favoriteActivities">Favorite Activities</Label>
                  <Textarea
                    id="favoriteActivities"
                    placeholder="Specific activities the child enjoys..."
                    value={favoriteActivities}
                    onChange={(e) => setFavoriteActivities(e.target.value)}
                    className="min-h-[120px] text-base"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <Button
                  onClick={() => setStep(1)}
                  variant="outline"
                  className="flex-1 rounded-full py-6 text-lg"
                  size="lg"
                >
                  Back
                </Button>
                <Button
                  onClick={() => setStep(3)}
                  disabled={!interests || !favoriteActivities}
                  className="flex-1 rounded-full py-6 text-lg"
                  size="lg"
                >
                  Next
                </Button>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6">
              <h1 className="text-3xl font-bold text-center text-foreground mb-6">
                Child Assessment
              </h1>

              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="autismSeverity">Autism Severity</Label>
                  <Select value={autismSeverity} onValueChange={setAutismSeverity}>
                    <SelectTrigger id="autismSeverity" className="text-base">
                      <SelectValue placeholder="Select..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="mild">Mild</SelectItem>
                      <SelectItem value="moderate">Moderate</SelectItem>
                      <SelectItem value="severe">Severe</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="communicationLevel">Communication Level</Label>
                  <Select value={communicationLevel} onValueChange={setCommunicationLevel}>
                    <SelectTrigger id="communicationLevel" className="text-base">
                      <SelectValue placeholder="Select..." />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="verbal">Verbal</SelectItem>
                      <SelectItem value="limited">Limited</SelectItem>
                      <SelectItem value="non-verbal">Non-verbal</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  onClick={() => setStep(2)}
                  variant="outline"
                  className="flex-1 rounded-full py-6 text-lg"
                  size="lg"
                >
                  Back
                </Button>
                {/* --- MODIFIED: Final button now shows loading state --- */}
                <Button
                  onClick={handleFinish}
                  disabled={!autismSeverity || !communicationLevel || isLoading}
                  className="flex-1 rounded-full py-6 text-lg bg-secondary hover:bg-secondary/90"
                  size="lg"
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                      Saving...
                    </>
                  ) : (
                    "Finish Setup!"
                  )}
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Onboarding;
