
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { AuthButton } from "@/components/auth-button";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { EnvVarWarning } from "@/components/env-var-warning";
import { hasEnvVars } from "@/lib/utils";// Lo incluimos para usar EnvVarWarning
import Link from "next/link";


export default async function PageLayout({
  children,
}: {
  children: React.ReactNode;
}) {
    const supabase = await createClient();

    const { data: { user } } = await supabase.auth.getUser();

    if (!user) {
        redirect("/auth/login");
    }

    const { data: officialData } = await supabase
        .from('officials')
        .select('full_name') 
        .eq('user_id', user.id)
        .single();
    
    const userName = officialData?.full_name || user.email || "Funcionario(a)";
    

    return (
        <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-black text-foreground">
            
            <nav className="w-full bg-white dark:bg-gray-800 border-b shadow-md p-4 flex justify-between items-center flex-shrink-0 px-8">
                
                <div className="flex items-center gap-6">
                    <h1 className="text-2xl font-bold text-blue-700">Dashboard de IA - Buenos Aires</h1>
                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        ¡Hola {userName}, bienvenido al portal de funcionarios!
                    </p>
                </div>
                
                <div>
                    {!hasEnvVars ? <EnvVarWarning /> : <AuthButton />}
                </div>
                
            </nav>

            <main className="flex-1 p-8 overflow-y-auto">
                {children} 
            </main>

            <footer className="w-full flex items-center justify-center border-t mx-auto text-center text-xs gap-8 py-4">
                 <p>
                    Powered by Supabase
                 </p>
                 <ThemeSwitcher />
            </footer>
        </div>
    );
}