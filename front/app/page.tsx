import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { hasEnvVars } from "@/lib/utils";
import Image from "next/image";
import Search from "@/components/ui/search";
import Floating_button from "@/components/ui/floating_button";

const monserrat = { className: 'font-extrabold' }; 

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center">
        <nav className="w-full flex justify-center border-b border-b-foreground/10 h-24">
          <div className="w-full max-w-full flex justify-between items-center px-5 text-sm">
            <div className="flex gap-5 items-center font-semibold">
              <Image
              src='/Logo.svg'
              alt='Logo Buenos Aires'
              width={80}
              height={80}
              className='hidden md:block'
              />
              <h1>Buenos Aires</h1>
            </div>
            {!hasEnvVars ? <EnvVarWarning /> : <AuthButton />}
          </div>
        </nav>
          <div className="relative flex-1 w-full flex items-center justify-center">
          
          <Image
            src='/BuenosAires.svg'
            alt='Foto Ciudad Buenos Aires'
            fill={true}
            className='hidden md:block absolute inset-0 object-cover' 
          />
          <div className="relative z-10 text-white text-center w-full max-w-2xl px-4">
        <h1 className="text-6xl font-extrabold mb-4 md:text-8xl md:mb-6">
            Buenos Aires
        </h1>
        
        <p className="text-xl mb-8 md:text-2xl md:mb-10">
            ¡a un clic y al toque!
        </p>

        <div className="flex justify-center">
            <Search placeholder="Buscar Trámites y Servicios..." />
        </div>
    </div>
          </div>

        <footer className="w-full flex justify-between items-center text-center text-xs border-t mx-auto px-5 py-8">
          <p>
            Powered by{" "}
            <a
              href="https://supabase.com/?utm_source=create-next-app&utm_medium=template&utm_term=nextjs"
              target="_blank"
              className="font-bold hover:underline"
              rel="noreferrer"
            >
              Supabase
            </a>
          </p>
          <ThemeSwitcher />
        </footer>
        <Floating_button />
    </main>
  );
}
