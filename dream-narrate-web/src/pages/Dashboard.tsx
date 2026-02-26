


// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Card, CardContent } from "@/components/ui/card";
// import { User, Loader2 } from "lucide-react"; // Import Loader2

// interface ChildProfile {
//   name: string;
//   age: string;
//   interests: string;
//   favoriteActivities: string;
//   autismSeverity: string;
//   communicationLevel: string;
// }

// const personalizedThemes = [
//   "Dinesh and Daniel go on a train adventure",
//   "The Lost Dinosaur Egg",
//   "Leo's First Day at Space School",
// ];

// const educationalThemes = [
//   "Learning about money management",
//   "The power of sharing",
//   "How to be a good friend",
// ];

// // --- NEW: Define API Base URL (Make sure VITE_API_BASE_URL is in your .env file) ---
// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// const Dashboard = () => {
//   const navigate = useNavigate();
//   const [profile, setProfile] = useState<ChildProfile | null>(null);
//   const [selectedPersonalized, setSelectedPersonalized] = useState<string | null>(
//     null
//   );
//   const [selectedEducational, setSelectedEducational] = useState<string | null>(
//     null
//   );
//   const [isLoading, setIsLoading] = useState(false);

//   useEffect(() => {
//     const storedProfile = localStorage.getItem("childProfile");
//     if (storedProfile) {
//       setProfile(JSON.parse(storedProfile));
//     } else {
//       // Redirect to onboarding if no profile found
//       navigate("/"); // Assuming '/' is your onboarding route
//     }
//   }, [navigate]);

//   const handleStartStory = async () => {
//     if (!selectedPersonalized || !selectedEducational) {
//       alert("Please select one personalized and one educational theme.");
//       return;
//     }
//     setIsLoading(true);
//     try {
//       // --- MODIFIED: Use API_BASE_URL ---
//       const response = await fetch(`${API_BASE_URL}/start-story`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           personalized_theme: selectedPersonalized,
//           educational_theme: selectedEducational,
//           language: "English", // Or get from user profile/settings
//           art_style_guide:
//             "A simple, friendly, and colorful children's book illustration. Use soft, clean lines, vibrant colors, and a happy tone.",
//         }),
//       });

//       if (!response.ok) {
//         // --- IMPROVED: Try to get error message from backend ---
//         const errorData = await response.json().catch(() => ({})); // Try parsing JSON, default to empty object
//         throw new Error(
//           errorData.detail || `HTTP error! Status: ${response.status}`
//         );
//       }

//       const storyData = await response.json();

//       console.log("Received initial story data:", storyData);

//       // --- CRITICAL: Ensure backend returns expected structure ---
//       if (!storyData || !storyData.story_part_data || !storyData.one_line_plan) {
//          throw new Error("Invalid story data received from server.");
//       }


//       // Navigate to the story page, passing the initial data
//       // --- Make sure your router is configured for a '/story' path ---
//       navigate("/story", { state: { initialStoryData: storyData } });

//     } catch (error) {
//       console.error("Error starting story:", error);
//       alert(
//         `Could not start the story. Please check the backend connection and try again. Error: ${
//           error instanceof Error ? error.message : String(error)
//         }`
//       );
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // --- Show loading or redirect message until profile loads ---
//   if (!profile) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <Loader2 className="w-8 h-8 animate-spin" />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen pb-12 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50"> {/* Added background gradient */}
//       <header className="bg-card shadow-sm border-b border-border sticky top-0 z-10"> {/* Made header sticky */}
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between"> {/* Adjusted padding */}
//           <h1 className="text-3xl font-bold text-primary tracking-tight"> {/* Adjusted size and color */}
//             StoryWeaver
//           </h1>
//           <Button
//             variant="ghost"
//             size="icon"
//             onClick={() => navigate("/profile")} // Assuming you have a profile page route
//             className="rounded-full hover:bg-muted"
//             aria-label="View Profile"
//           >
//             <User className="w-6 h-6 text-muted-foreground hover:text-foreground" />
//           </Button>
//         </div>
//       </header>

//       <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12"> {/* Adjusted padding */}
//         {/* Child Profile Display */}
//          <Card className="mb-8 p-6 bg-white/80 backdrop-blur-sm">
//            <h2 className="text-xl font-semibold text-foreground mb-4">Reading For:</h2>
//            <div className="flex items-center space-x-4">
//              <div className="bg-primary text-primary-foreground rounded-full p-3">
//                <User className="w-6 h-6" />
//              </div>
//              <div>
//                <p className="text-lg font-medium">{profile.name}</p>
//                <p className="text-sm text-muted-foreground">Age: {profile.age} | Interests: {profile.interests}</p>
//              </div>
//            </div>
//          </Card>

//         <section>
//           <h2 className="text-2xl font-bold text-foreground mb-2">
//             Choose a Personalized Theme
//           </h2>
//           <p className="text-muted-foreground mb-6">
//             What kind of adventure should we have?
//           </p>
//           {/* --- Added horizontal scroll container for better mobile view --- */}
//           <div className="flex space-x-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-muted-foreground scrollbar-track-muted">
//             {personalizedThemes.map((theme, index) => (
//               <Card
//                 key={index}
//                 onClick={() => setSelectedPersonalized(theme)}
//                 className={`flex-shrink-0 w-72 cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
//                   selectedPersonalized === theme
//                     ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl" // Enhanced selected state
//                     : "bg-card"
//                 }`}
//               >
//                 <CardContent className="p-6">
//                   <div className="h-28 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg mb-4 flex items-center justify-center">
//                     <p className="text-4xl">📚</p> {/* Example Icon */}
//                   </div>
//                   <h3 className="text-base font-semibold text-foreground text-center"> {/* Centered Text */}
//                     {theme}
//                   </h3>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </section>

//         <section>
//           <h2 className="text-2xl font-bold text-foreground mb-2">
//             Choose an Educational Theme
//           </h2>
//           <p className="text-muted-foreground mb-6">
//             What lesson can we learn along the way?
//           </p>
//           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"> {/* Responsive Grid */}
//             {educationalThemes.map((theme, index) => (
//               <Card
//                 key={index}
//                 onClick={() => setSelectedEducational(theme)}
//                  className={`cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
//                   selectedEducational === theme
//                     ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl" // Enhanced selected state
//                     : "bg-card"
//                 }`}
//               >
//                 <CardContent className="p-6">
//                   <div className="h-28 bg-gradient-to-br from-accent/20 to-primary/10 rounded-lg mb-4 flex items-center justify-center">
//                     <p className="text-4xl">🎓</p> {/* Example Icon */}
//                   </div>
//                   <h3 className="text-base font-semibold text-foreground text-center"> {/* Centered Text */}
//                     {theme}
//                   </h3>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </section>

//         <div className="flex justify-center pt-8">
//           <Button
//             onClick={handleStartStory}
//             disabled={isLoading || !selectedPersonalized || !selectedEducational}
//             className="rounded-full px-12 py-6 text-xl bg-gradient-to-r from-primary to-secondary text-primary-foreground shadow-lg hover:shadow-xl hover:scale-105 transform transition-all duration-300 disabled:opacity-50 disabled:scale-100 disabled:shadow-none" // Enhanced styling
//             size="lg"
//           >
//             {isLoading ? (
//               <>
//                 <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Generating...
//               </>
//             ) : (
//               "Start Story!"
//             )}
//           </Button>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Dashboard;

// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Card, CardContent } from "@/components/ui/card";
// import { User, Loader2 } from "lucide-react";

// interface ChildProfile {
//   id: number;
//   name: string;
//   age: number;
//   interests: string;
//   favorite_activities: string;
//   autism_severity: string;
//   communication_level: string;
//   personalized_themes: string[];
// }

// // --- MODIFIED: Replaced emojis with image URLs for flags ---
// const supportedLanguages = [
//     { code: "English", name: "English", imageUrl: "https://flagcdn.com/gb.svg" },
//     { code: "tamil", name: "Tamil", imageUrl: "https://flagcdn.com/in.svg" },
//     // You can add more languages with their respective flag image URLs
//     // { code: "es-ES", name: "Español", imageUrl: "https://flagcdn.com/es.svg" },
//     // { code: "fr-FR", name: "Français", imageUrl: "https://flagcdn.com/fr.svg" },
// ];


// const educationalThemes = [
//   "Learning about money management",
//   "The power of sharing",
//   "How to be a good friend",
// ];

// const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// const Dashboard = () => {
//   const navigate = useNavigate();
//   const [profile, setProfile] = useState<ChildProfile | null>(null);
//   const [selectedPersonalized, setSelectedPersonalized] = useState<string | null>(null);
//   const [selectedEducational, setSelectedEducational] = useState<string | null>(null);
//   const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
//   const [isLoading, setIsLoading] = useState(false);
//   const [isProfileLoading, setIsProfileLoading] = useState(true);

//   useEffect(() => {
//     const fetchProfile = async () => {
//       try {
//         const response = await fetch(`${API_BASE_URL}/profile`);
//         if (!response.ok) {
//           if (response.status === 404) {
//             navigate("/");
//             return;
//           }
//           throw new Error("Failed to fetch profile");
//         }
//         const profileData = await response.json();
//         setProfile(profileData);
//       } catch (error) {
//         console.error("Error fetching profile:", error);
//         navigate("/");
//       } finally {
//         setIsProfileLoading(false);
//       }
//     };

//     fetchProfile();
//   }, [navigate]);

//   const handleStartStory = async () => {
//     if (!selectedPersonalized || !selectedEducational || !selectedLanguage) {
//       alert("Please select a personalized theme, an educational theme, and a language.");
//       return;
//     }
//     setIsLoading(true);
//     try {
//       const response = await fetch(`${API_BASE_URL}/start-story`, {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           personalized_theme: selectedPersonalized,
//           educational_theme: selectedEducational,
//           language: selectedLanguage,
//           art_style_guide: "A simple, friendly, and colorful children's book illustration...",
//         }),
//       });
//       if (!response.ok) {
//         const errorData = await response.json().catch(() => ({}));
//         throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
//       }
//       const storyData = await response.json();
//       if (!storyData || !storyData.story_part_data || !storyData.one_line_plan) {
//          throw new Error("Invalid story data received from server.");
//       }
//       navigate("/story", { state: { initialStoryData: storyData } });
//     } catch (error) {
//       console.error("Error starting story:", error);
//       alert(`Could not start story. Error: ${error instanceof Error ? error.message : String(error)}`);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   if (isProfileLoading || !profile) {
//     return (
//       <div className="flex justify-center items-center min-h-screen">
//         <Loader2 className="w-8 h-8 animate-spin" />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen pb-12 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
//       <header className="bg-card shadow-sm border-b border-border sticky top-0 z-10">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
//           <h1 className="text-3xl font-bold text-primary tracking-tight">
//             StoryWeaver
//           </h1>
//           <Button
//             variant="ghost"
//             size="icon"
//             onClick={() => navigate("/profile")}
//             className="rounded-full hover:bg-muted"
//             aria-label="View Profile"
//           >
//             <User className="w-6 h-6 text-muted-foreground hover:text-foreground" />
//           </Button>
//         </div>
//       </header>

//       <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
//         <Card className="mb-8 p-6 bg-white/80 backdrop-blur-sm">
//            <h2 className="text-xl font-semibold text-foreground mb-4">Reading For:</h2>
//            <div className="flex items-center space-x-4">
//              <div className="bg-primary text-primary-foreground rounded-full p-3">
//                <User className="w-6 h-6" />
//              </div>
//              <div>
//                <p className="text-lg font-medium">{profile.name}</p>
//                <p className="text-sm text-muted-foreground">Age: {profile.age} | Interests: {profile.interests}</p>
//              </div>
//            </div>
//          </Card>
        
//         <section>
//           <h2 className="text-2xl font-bold text-foreground mb-2">
//             Choose a Language
//           </h2>
//            <p className="text-muted-foreground mb-6">
//             In which language should the story be told?
//           </p>
//           <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
//             {supportedLanguages.map((lang) => (
//               <Card
//                 key={lang.code}
//                 onClick={() => setSelectedLanguage(lang.code)}
//                 className={`cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
//                   selectedLanguage === lang.code
//                     ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
//                     : "bg-card"
//                 }`}
//               >
//                 <CardContent className="p-6 flex flex-col items-center justify-center">
//                   {/* --- MODIFIED: Replaced <p> with <img> to render flag image --- */}
//                   <img
//                     src={lang.imageUrl}
//                     alt={`${lang.name} flag`}
//                     className="w-16 h-12 mb-4 rounded-md object-cover shadow-sm"
//                   />
//                   <h3 className="text-base font-semibold text-foreground text-center">
//                     {lang.name}
//                   </h3>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </section>

//         <section>
//           <h2 className="text-2xl font-bold text-foreground mb-2">
//             Choose a Personalized Theme
//           </h2>
//           <p className="text-muted-foreground mb-6">
//             What kind of adventure should we have?
//           </p>
//           <div className="flex space-x-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-muted-foreground scrollbar-track-muted">
//             {profile.personalized_themes.length > 0 ? (
//                 profile.personalized_themes.map((theme, index) => (
//               <Card
//                 key={index}
//                 onClick={() => setSelectedPersonalized(theme)}
//                 className={`flex-shrink-0 w-72 cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
//                   selectedPersonalized === theme
//                     ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
//                     : "bg-card"
//                 }`}
//               >
//                 <CardContent className="p-6">
//                   <div className="h-28 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg mb-4 flex items-center justify-center">
//                     <p className="text-4xl">📚</p>
//                   </div>
//                   <h3 className="text-base font-semibold text-foreground text-center">
//                     {theme}
//                   </h3>
//                 </CardContent>
//               </Card>
//             ))
//             ) : (
//                 <p className="text-muted-foreground">No personalized themes were found for this profile.</p>
//             )}
//           </div>
//         </section>

//         <section>
//           <h2 className="text-2xl font-bold text-foreground mb-2">
//             Choose an Educational Theme
//           </h2>
//           <p className="text-muted-foreground mb-6">
//             What lesson can we learn along the way?
//           </p>
//           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
//             {educationalThemes.map((theme, index) => (
//               <Card
//                 key={index}
//                 onClick={() => setSelectedEducational(theme)}
//                 className={`cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
//                   selectedEducational === theme
//                     ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
//                     : "bg-card"
//                 }`}
//               >
//                 <CardContent className="p-6">
//                   <div className="h-28 bg-gradient-to-br from-accent/20 to-primary/10 rounded-lg mb-4 flex items-center justify-center">
//                     <p className="text-4xl">🎓</p>
//                   </div>
//                   <h3 className="text-base font-semibold text-foreground text-center">
//                     {theme}
//                   </h3>
//                 </CardContent>
//               </Card>
//             ))}
//           </div>
//         </section>

//         <div className="flex justify-center pt-8">
//           <Button
//             onClick={handleStartStory}
//             disabled={isLoading || !selectedPersonalized || !selectedEducational || !selectedLanguage}
//             className="rounded-full px-12 py-6 text-xl bg-gradient-to-r from-primary to-secondary text-primary-foreground shadow-lg hover:shadow-xl hover:scale-105 transform transition-all duration-300 disabled:opacity-50 disabled:scale-100 disabled:shadow-none"
//             size="lg"
//           >
//             {isLoading ? (
//               <>
//                 <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Generating...
//               </>
//             ) : (
//               "Start Story!"
//             )}
//           </Button>
//         </div>
//       </main>
//     </div>
//   );
// };

// export default Dashboard;

import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { User, Loader2 } from "lucide-react";

interface ChildProfile {
  id: number;
  name: string;
  age: number;
  interests: string;
  favorite_activities: string;
  autism_severity: string;
  communication_level: string;
  personalized_themes: string[];
}

const supportedLanguages = [
    { code: "English", name: "English", imageUrl: "https://flagcdn.com/gb.svg" },
    { code: "tamil", name: "Tamil ", imageUrl: "https://flagcdn.com/in.svg" },
    { code: "Tanglish", name: "Tanglish", imageUrl: "https://flagcdn.com/in.svg" },
];


const educationalThemes = [
  "Learning about money management",
  "The power of sharing",
  "How to be a good friend",
];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

const Dashboard = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<ChildProfile | null>(null);
  const [selectedPersonalized, setSelectedPersonalized] = useState<string | null>(null);
  const [selectedEducational, setSelectedEducational] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isProfileLoading, setIsProfileLoading] = useState(true);

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/profile`);
        if (!response.ok) {
          if (response.status === 404) {
            navigate("/");
            return;
          }
          throw new Error("Failed to fetch profile");
        }
        const profileData = await response.json();
        setProfile(profileData);
      } catch (error) {
        console.error("Error fetching profile:", error);
        navigate("/");
      } finally {
        setIsProfileLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleStartStory = async () => {
    if (!selectedPersonalized || !selectedEducational || !selectedLanguage) {
      alert("Please select a personalized theme, an educational theme, and a language.");
      return;
    }
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/start-story`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          personalized_theme: selectedPersonalized,
          educational_theme: selectedEducational,
          language: selectedLanguage,
          art_style_guide: "A simple, friendly, and colorful children's book illustration...",
        }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! Status: ${response.status}`);
      }
      const storyData = await response.json();
      if (!storyData || !storyData.story_part_data || !storyData.one_line_plan) {
         throw new Error("Invalid story data received from server.");
      }
      
      // --- MODIFIED: Pass the selected language in the navigation state ---
      navigate("/story", { state: { initialStoryData: storyData, language: selectedLanguage } });

    } catch (error) {
      console.error("Error starting story:", error);
      alert(`Could not start story. Error: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setIsLoading(false);
    }
  };

  if (isProfileLoading || !profile) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-12 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      <header className="bg-card shadow-sm border-b border-border sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-primary tracking-tight">
            StoryWeaver
          </h1>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => navigate("/profile")}
            className="rounded-full hover:bg-muted"
            aria-label="View Profile"
          >
            <User className="w-6 h-6 text-muted-foreground hover:text-foreground" />
          </Button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        <Card className="mb-8 p-6 bg-white/80 backdrop-blur-sm">
           <h2 className="text-xl font-semibold text-foreground mb-4">Reading For:</h2>
           <div className="flex items-center space-x-4">
             <div className="bg-primary text-primary-foreground rounded-full p-3">
               <User className="w-6 h-6" />
             </div>
             <div>
               <p className="text-lg font-medium">{profile.name}</p>
               <p className="text-sm text-muted-foreground">Age: {profile.age} | Interests: {profile.interests}</p>
             </div>
           </div>
         </Card>
        
        <section>
          <h2 className="text-2xl font-bold text-foreground mb-2">
            Choose a Language
          </h2>
           <p className="text-muted-foreground mb-6">
            In which language should the story be told?
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {supportedLanguages.map((lang) => (
              <Card
                key={lang.code}
                onClick={() => setSelectedLanguage(lang.code)}
                className={`cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
                  selectedLanguage === lang.code
                    ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
                    : "bg-card"
                }`}
              >
                <CardContent className="p-6 flex flex-col items-center justify-center">
                  <img
                    src={lang.imageUrl}
                    alt={`${lang.name} flag`}
                    className="w-16 h-12 mb-4 rounded-md object-cover shadow-sm"
                  />
                  <h3 className="text-base font-semibold text-foreground text-center">
                    {lang.name}
                  </h3>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-foreground mb-2">
            Choose a Personalized Theme
          </h2>
          <p className="text-muted-foreground mb-6">
            What kind of adventure should we have?
          </p>
          <div className="flex space-x-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-muted-foreground scrollbar-track-muted">
            {profile.personalized_themes.length > 0 ? (
                profile.personalized_themes.map((theme, index) => (
              <Card
                key={index}
                onClick={() => setSelectedPersonalized(theme)}
                className={`flex-shrink-0 w-72 cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
                  selectedPersonalized === theme
                    ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
                    : "bg-card"
                }`}
              >
                <CardContent className="p-6">
                  <div className="h-28 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-lg mb-4 flex items-center justify-center">
                    <p className="text-4xl">📚</p>
                  </div>
                  <h3 className="text-base font-semibold text-foreground text-center">
                    {theme}
                  </h3>
                </CardContent>
              </Card>
            ))
            ) : (
                <p className="text-muted-foreground">No personalized themes were found for this profile.</p>
            )}
          </div>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-foreground mb-2">
            Choose an Educational Theme
          </h2>
          <p className="text-muted-foreground mb-6">
            What lesson can we learn along the way?
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {educationalThemes.map((theme, index) => (
              <Card
                key={index}
                onClick={() => setSelectedEducational(theme)}
                className={`cursor-pointer transition-all duration-300 ease-in-out hover:shadow-lg hover:-translate-y-1 ${
                  selectedEducational === theme
                    ? "ring-2 ring-primary ring-offset-2 scale-105 shadow-xl"
                    : "bg-card"
                }`}
              >
                <CardContent className="p-6">
                  <div className="h-28 bg-gradient-to-br from-accent/20 to-primary/10 rounded-lg mb-4 flex items-center justify-center">
                    <p className="text-4xl">🎓</p>
                  </div>
                  <h3 className="text-base font-semibold text-foreground text-center">
                    {theme}
                  </h3>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>

        <div className="flex justify-center pt-8">
          <Button
            onClick={handleStartStory}
            disabled={isLoading || !selectedPersonalized || !selectedEducational || !selectedLanguage}
            className="rounded-full px-12 py-6 text-xl bg-gradient-to-r from-primary to-secondary text-primary-foreground shadow-lg hover:shadow-xl hover:scale-105 transform transition-all duration-300 disabled:opacity-50 disabled:scale-100 disabled:shadow-none"
            size="lg"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Generating...
              </>
            ) : (
              "Start Story!"
            )}
          </Button>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

