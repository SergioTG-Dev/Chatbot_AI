import { NextRequest } from 'next/server'

export async function GET(_req: NextRequest) {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'
  const target = `${baseUrl}/api/v1/departments`
  try {
    const resp = await fetch(target, {
      headers: { accept: 'application/json' },
      cache: 'no-store',
    })
    if (!resp.ok) {
      const text = await resp.text().catch(() => '')
      console.error('[proxy] departments fetch failed', { status: resp.status, body: text, target })
      return new Response(
        JSON.stringify({ error: 'Backend departments fetch failed', status: resp.status, body: text }),
        { status: 502, headers: { 'content-type': 'application/json' } }
      )
    }
    const data = await resp.json()
    return new Response(JSON.stringify(Array.isArray(data) ? data : []), {
      status: 200,
      headers: { 'content-type': 'application/json' },
    })
  } catch (e: any) {
    console.error('[proxy] departments error', e?.message ?? e)
    return new Response(
      JSON.stringify({ error: 'Proxy request failed', message: e?.message ?? 'Unknown error' }),
      { status: 502, headers: { 'content-type': 'application/json' } }
    )
  }
}