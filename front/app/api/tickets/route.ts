import { NextResponse } from "next/server"
import { createClient } from "@/lib/supabase/server"

// Crear ticket
export async function POST(req: Request) {
  try {
    const { dni, service } = await req.json()

    if (!dni || !service) {
      return NextResponse.json({ error: "Missing parameters" }, { status: 400 })
    }

    // Validar que el ciudadano exista
    const supabase = await createClient()
    const { data: citizen, error: citizenError } = await supabase
      .from("citizens")
      .select("id, first_name, last_name")
      .eq("dni", dni)
      .single()

    if (citizenError || !citizen) {
      return NextResponse.json(
        { error: "Citizen not found" },
        { status: 404 }
      )
    }

    // Crear ticket asociado al citizen_id
    const { data: ticket, error: ticketError } = await supabase
      .from("tickets")
      .insert([{ citizen_id: citizen.id, service }])
      .select()
      .single()

    if (ticketError) throw ticketError

    return NextResponse.json(
      { ticket, citizen },
      { status: 201 }
    )
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}

// Listar todos los tickets
export async function GET() {
  try {
    const supabase = await createClient()
    const { data, error } = await supabase
      .from("tickets")
      .select("id, service, status, created_at, citizens(dni, first_name, last_name)")

    if (error) throw error

    return NextResponse.json({ tickets: data }, { status: 200 })
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}