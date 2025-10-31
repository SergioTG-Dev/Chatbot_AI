import Link from "next/link";
import { Button } from "./ui/button";
import { createClient } from "@/lib/supabase/server";
import { LogoutButton } from "./logout-button";
import { ThemeSwitcher } from "./theme-switcher";

export async function AuthButton() {
  const supabase = await createClient();

  // Obtener el usuario autenticado
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return (
      <div className="flex gap-2">
        <Button asChild size="sm" variant={"outline"}>
          <Link href="/auth/login">Login</Link>
        </Button>
      </div>
    );
  }

  // Buscar información del funcionario (tabla 'officials')
  const { data: official, error } = await supabase
    .from("officials")
    .select("full_name, role, department_id, description")
    .eq("id", user.id) // Relación con auth.users.id
    .single();

  if (error) {
    console.error("Error al obtener official:", error);
  }

  // Renderizado según el rol
  if (official?.role === "admin") {
    return (
      <div className="flex items-center gap-4">
        👑 Bienvenido administrador {official.full_name || user.email}
        <Button asChild size="sm" variant="secondary">
        <Link href="/admin/dashboard">Ir al panel</Link>
        </Button>
        <div className="flex items-center gap-2">
          <LogoutButton />
          <ThemeSwitcher />
        </div>
      </div>
    );
  }

  if (official?.role === "funcionario") {
    return (
      <div className="flex items-center gap-4">
        👋 Hola {official.full_name || user.email}, bienvenido al portal de funcionarios
        <Button asChild size="sm" variant="secondary">
          <Link href="/admin/dashboard">Ir a mi panel</Link>
        </Button>
        <div className="flex items-center gap-2">
          <LogoutButton />
          <ThemeSwitcher />
        </div>
      </div>
    );
  }

  // Por defecto (usuario sin rol asignado)
  return (
    <div className="flex items-center gap-4">
      Hey, {user.email}!
      <div className="flex items-center gap-2">
        <LogoutButton />
        <ThemeSwitcher />
      </div>
    </div>
  );
}
