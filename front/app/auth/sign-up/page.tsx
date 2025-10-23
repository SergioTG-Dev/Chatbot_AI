"use client";

import { SignUpForm } from "@/components/sign-up-form";
import { createClient } from "@/lib/supabase/client";
import { useState } from "react";

export default function Page() {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (error) {
    console.error(error);
  }

  return (
    <div className="flex min-h-svh w-full items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm">
        <SignUpForm />
      </div>
      {loading && <p>Loading...</p>}
      {error && <p>{error}</p>}
    </div>
  );
}
