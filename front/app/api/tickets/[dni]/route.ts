import { NextResponse } from "next/server"
import { createClient } from "@/lib/supabase/server"

export async function GET(
  req: Request,
  { params }: { params: Promise<{ dni: string }> }
) {
  try {
    const { dni } = await params

    // Buscar ciudadano
    const supabase = await createClient()
    const { data: citizen, error: citizenError } = await supabase
      .from("citizens")
      .select("id")
      .eq("dni", dni)
      .single()

    if (citizenError || !citizen) {
      return NextResponse.json({ error: "Citizen not found" }, { status: 404 })
    }

    // Buscar tickets del ciudadano
    const { data: tickets, error: ticketError } = await supabase
      .from("tickets")
      .select("*")
      .eq("citizen_id", citizen.id)

    if (ticketError) throw ticketError

    return NextResponse.json({ tickets }, { status: 200 })
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 })
  }
}
