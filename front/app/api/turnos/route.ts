import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
    const target = `${baseUrl}/api/v1/turnos/`
    const body = await req.text()

    const resp = await fetch(target, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        accept: 'application/json',
      },
      body,
      cache: 'no-store',
    })

    const text = await resp.text().catch(() => '')
    const contentType = resp.headers.get('content-type') || ''

    if (!resp.ok) {
      // Propagar error en formato JSON consistente
      let json: any = undefined
      if (contentType.includes('application/json')) {
        try { json = JSON.parse(text) } catch {}
      }
      return new Response(
        JSON.stringify({ error: 'Backend turno creation failed', status: resp.status, body: json ?? text }),
        { status: resp.status, headers: { 'content-type': 'application/json' } }
      )
    }

    // Éxito: devolver JSON tal cual
    if (contentType.includes('application/json')) {
      return new Response(text, { status: 201, headers: { 'content-type': 'application/json' } })
    }
    // Si el backend no devolvió JSON, normalizar a objeto
    return new Response(JSON.stringify({ message: 'Turno creado', body: text }), {
      status: 201,
      headers: { 'content-type': 'application/json' },
    })
  } catch (e: any) {
    console.error('[proxy] turnos POST error', e?.message ?? e)
    return new Response(
      JSON.stringify({ error: 'Proxy request failed', message: e?.message ?? 'Unknown error' }),
      { status: 502, headers: { 'content-type': 'application/json' } }
    )
  }
}