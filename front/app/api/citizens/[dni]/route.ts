import { NextRequest } from 'next/server'

export async function GET(_req: NextRequest, { params }: { params: Promise<{ dni: string }> }) {
  const { dni } = await params
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
  const target = `${baseUrl}/api/v1/citizens/${dni}`
  try {
    const resp = await fetch(target, {
      headers: { accept: 'application/json' },
      cache: 'no-store',
    })
    const text = await resp.text().catch(() => '')
    const contentType = resp.headers.get('content-type') || ''

    if (!resp.ok) {
      let body: any = text
      if (contentType.includes('application/json')) {
        try { body = JSON.parse(text) } catch {}
      }
      return new Response(
        JSON.stringify({ error: 'Citizen lookup failed', status: resp.status, body }),
        { status: resp.status, headers: { 'content-type': 'application/json' } }
      )
    }

    return new Response(text, { status: 200, headers: { 'content-type': 'application/json' } })
  } catch (e: any) {
    console.error('[proxy] citizens GET error', e?.message ?? e)
    return new Response(
      JSON.stringify({ error: 'Proxy request failed', message: e?.message ?? 'Unknown error' }),
      { status: 502, headers: { 'content-type': 'application/json' } }
    )
  }
}