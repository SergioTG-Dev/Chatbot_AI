"use client";

import { SignUpForm } from "@/components/sign-up-form";
import { createClient } from "@/lib/supabase/client";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function Page() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const signUpWithGoogle = async () => {
    const supabase = createClient();
    setLoading(true);
    try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    });
    if (error) {
        setError(error.message);
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  if (error) {
    console.error(error);
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <SignUpForm />
        <Button onClick={signUpWithGoogle}>Sign up with Google</Button>
      </div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
    </div>
  );
}
