import Link from "next/link";
import { Button } from "./ui/button";
import { createClient } from "@/lib/supabase/server";
import { LogoutButton } from "./logout-button";

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
        <Button asChild size="sm" variant="secondary">
          <Link href="/admin">Ir al panel</Link>
        </Button>
        <LogoutButton />
      </div>
    );
  }

  if (official?.role === "funcionario") {
    return (
      <div className="flex items-center gap-4">
        <Button asChild size="sm" variant="secondary">
          <Link href="/funcionario/inicio">Ir a mi panel</Link>
        </Button>
        <LogoutButton />
      </div>
    );
  }

  // Por defecto (usuario sin rol asignado)
  return (
    <div className="flex items-center gap-4">
      Hey, {user.email}!
      <LogoutButton />
    </div>
  );
}
