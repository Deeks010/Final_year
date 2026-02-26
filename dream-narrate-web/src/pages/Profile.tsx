// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
// import { Button } from "@/components/ui/button";
// import { Card, CardContent } from "@/components/ui/card";
// import { Edit, ArrowLeft } from "lucide-react";

// interface ChildProfile {
//   name: string;
//   age: string;
//   interests: string;
//   favoriteActivities: string;
//   autismSeverity: string;
//   communicationLevel: string;
// }

// const Profile = () => {
//   const navigate = useNavigate();
//   const [profile, setProfile] = useState<ChildProfile | null>(null);

//   useEffect(() => {
//     const storedProfile = localStorage.getItem("childProfile");
//     if (storedProfile) {
//       setProfile(JSON.parse(storedProfile));
//     } else {
//       navigate("/");
//     }
//   }, [navigate]);

//   if (!profile) return null;

//   return (
//     <div className="min-h-screen pb-12">
//       <header className="bg-card shadow-sm border-b border-border">
//         <div className="max-w-7xl mx-auto px-4 py-6 flex items-center justify-between">
//           <Button
//             variant="ghost"
//             size="sm"
//             onClick={() => navigate("/dashboard")}
//             className="gap-2"
//           >
//             <ArrowLeft className="w-4 h-4" />
//             Back to Dashboard
//           </Button>
//           <h1 className="text-4xl font-bold text-foreground">Child Profile</h1>
//           <div className="w-32" />
//         </div>
//       </header>

//       <main className="max-w-4xl mx-auto px-4 py-12">
//         <Card>
//           <CardContent className="p-8">
//             <div className="flex items-start justify-between mb-8">
//               <h2 className="text-3xl font-bold text-foreground">
//                 {profile.name}
//               </h2>
//               <Button
//                 variant="outline"
//                 size="sm"
//                 onClick={() => navigate("/")}
//                 className="rounded-full gap-2"
//               >
//                 <Edit className="w-4 h-4" />
//                 Edit Profile
//               </Button>
//             </div>

//             <div className="grid md:grid-cols-2 gap-6">
//               <div className="space-y-2">
//                 <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
//                   Age
//                 </p>
//                 <p className="text-lg text-foreground">{profile.age} years old</p>
//               </div>

//               {profile.autismSeverity && (
//                 <div className="space-y-2">
//                   <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
//                     Autism Severity
//                   </p>
//                   <p className="text-lg text-foreground capitalize">{profile.autismSeverity}</p>
//                 </div>
//               )}

//               {profile.communicationLevel && (
//                 <div className="space-y-2">
//                   <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
//                     Communication Level
//                   </p>
//                   <p className="text-lg text-foreground capitalize">
//                     {profile.communicationLevel.replace("-", " ")}
//                   </p>
//                 </div>
//               )}

//               {profile.interests && (
//                 <div className="space-y-2 md:col-span-2">
//                   <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
//                     Interests & Preferences
//                   </p>
//                   <p className="text-base text-foreground leading-relaxed">
//                     {profile.interests}
//                   </p>
//                 </div>
//               )}

//               {profile.favoriteActivities && (
//                 <div className="space-y-2 md:col-span-2">
//                   <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
//                     Favorite Activities
//                   </p>
//                   <p className="text-base text-foreground leading-relaxed">
//                     {profile.favoriteActivities}
//                   </p>
//                 </div>
//               )}
//             </div>
//           </CardContent>
//         </Card>
//       </main>
//     </div>
//   );
// };

// export default Profile;


import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Edit, ArrowLeft, Loader2 } from "lucide-react";

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

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin;

const Profile = () => {
  const navigate = useNavigate();
  const [profile, setProfile] = useState<ChildProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true); // --- NEW: Loading state ---

  // --- MODIFIED: Fetch profile from backend instead of localStorage ---
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/profile`);
        if (!response.ok) {
          if (response.status === 404) {
            navigate("/"); // No profile, go to onboarding
            return;
          }
          throw new Error("Failed to fetch profile");
        }
        const profileData = await response.json();
        setProfile(profileData);
      } catch (error) {
        console.error("Error fetching profile:", error);
        navigate("/"); // On error, go to onboarding
      } finally {
        setIsLoading(false);
      }
    };

    fetchProfile();
  }, [navigate]);

  // --- MODIFIED: Show loader while fetching ---
  if (isLoading || !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-12 bg-gray-50">
      <header className="bg-card shadow-sm border-b border-border">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/dashboard")}
            className="gap-2 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Dashboard
          </Button>
          <h1 className="text-2xl font-bold text-foreground">Child Profile</h1>
          {/* Empty div for alignment */}
          <div style={{ width: '150px' }} /> 
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-12">
        <Card>
          <CardContent className="p-8">
            <div className="flex items-start justify-between mb-8">
              <h2 className="text-3xl font-bold text-foreground">
                {profile.name}
              </h2>
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate("/")} // Navigate to onboarding to "edit"
                className="rounded-full gap-2"
              >
                <Edit className="w-4 h-4" />
                Re-Onboard
              </Button>
            </div>

            <div className="grid md:grid-cols-2 gap-x-8 gap-y-6">
              <div className="space-y-1">
                <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                  Age
                </p>
                <p className="text-lg text-foreground">{profile.age} years old</p>
              </div>

              {profile.autism_severity && (
                <div className="space-y-1">
                  <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                    Autism Severity
                  </p>
                  <p className="text-lg text-foreground capitalize">{profile.autism_severity}</p>
                </div>
              )}

              {profile.communication_level && (
                <div className="space-y-1">
                  <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                    Communication Level
                  </p>
                  <p className="text-lg text-foreground capitalize">
                    {profile.communication_level.replace("-", " ")}
                  </p>
                </div>
              )}

              <div className="space-y-1 md:col-span-2 pt-4">
                 <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                   Generated Personalized Themes
                 </p>
                 {profile.personalized_themes && profile.personalized_themes.length > 0 ? (
                    <ul className="list-disc list-inside space-y-1 pt-2 text-base text-foreground">
                        {profile.personalized_themes.map((theme, i) => <li key={i}>{theme}</li>)}
                    </ul>
                 ) : (
                    <p className="text-base text-muted-foreground italic">No themes were generated.</p>
                 )}
              </div>

              {profile.interests && (
                <div className="space-y-1 md:col-span-2 pt-4">
                  <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                    Interests & Preferences
                  </p>
                  <p className="text-base text-foreground leading-relaxed">
                    {profile.interests}
                  </p>
                </div>
              )}

              {profile.favorite_activities && (
                <div className="space-y-1 md:col-span-2 pt-4">
                  <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide">
                    Favorite Activities
                  </p>
                  <p className="text-base text-foreground leading-relaxed">
                    {profile.favorite_activities}
                  </p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default Profile;
