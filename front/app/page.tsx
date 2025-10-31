import { EnvVarWarning } from "@/components/env-var-warning";
import { AuthButton } from "@/components/auth-button";
// ThemeSwitcher ahora se renderiza junto al Logout en la barra superior
import { hasEnvVars } from "@/lib/utils";
import Image from "next/image";
import { Suspense } from "react";
import Search from "@/components/ui/search";
import Floating_button from "@/components/ui/floating_button";

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
          {/* Superposición para mejorar contraste del texto sobre la imagen */}
          <div className='hidden md:block absolute inset-0 bg-black/40' aria-hidden='true'></div>
          <div className="relative z-10 text-white text-center w-full max-w-2xl px-4 md:bg-black/30 md:backdrop-blur-sm md:rounded-xl md:p-6 md:shadow-lg">
        <h1 className="text-1xl font-extrabold mb-4 md:text-3xl md:mb-6 drop-shadow-xl">
            Bienvenidos al portal de Buenos Aires
        </h1>

        <p className="text-2xl mb-2 md:text-2xl md:mb-3 drop-shadow-md">
            Habla con CiviBot para gestionar trámites, pedir turnos, consultar información y reportar emergencias.
        </p>
        <p className="text-sm mb-8 md:text-base md:mb-10 opacity-90 drop-shadow-md">
            Tu asistente virtual municipal disponible 24/7.
        </p>

        <div className="flex justify-center">
            <Suspense fallback={<div className="text-white/90">Cargando búsqueda...</div>}>
              <Search placeholder="Buscar Trámites y Servicios..." />
            </Suspense>
        </div>
    </div>
          </div>

        <footer className="w-full flex justify-between items-center text-center text-xs border-t mx-auto px-5 py-8">
          {/* Footer de producción sin branding externo */}
          {/* ThemeSwitcher movido a la barra superior */}
        </footer>
        <Floating_button />
    </main>
  );
}
