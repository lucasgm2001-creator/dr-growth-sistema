// ============================================================
//  DR Growth — Webhook Receiver: Magnetic Funnels (HighLevel)
//  Endpoint: POST /functions/v1/magnetic-webhook
//
//  Configurar no Magnetic Funnels:
//    Automações > Webhook > URL: https://hevtlwnyarthvqmihsuk.supabase.co/functions/v1/magnetic-webhook
// ============================================================

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-ghl-signature',
}

// Campos do formulário Magnetic que mapeiam para campos do site
// Ajuste as chaves da esquerda conforme os nomes dos campos do seu formulário
const FIELD_MAP: Record<string, string> = {
  nome:    'name',
  name:    'name',
  email:   'email',
  telefone:'phone',
  phone:   'phone',
  empresa: 'company',
  company: 'company',
}

function extractContact(body: Record<string, unknown>) {
  // HighLevel pode enviar em vários formatos dependendo do trigger
  const contact = (body.contact as Record<string, unknown>) || body
  const formData = (body.form_data || body.formData || body.data || {}) as Record<string, unknown>

  // Nome: tenta campos em cascata
  const firstName = String(contact.firstName || contact.first_name || formData.nome || formData.name || '')
  const lastName  = String(contact.lastName  || contact.last_name  || '')
  const fullName  = String(contact.name      || formData.nome || formData.name || `${firstName} ${lastName}`.trim() || 'Sem nome')

  // Origem: tenta identificar a fonte
  const source = String(
    contact.source     ||
    body.source        ||
    contact.attributionSource ||
    'Magnetic Funnels'
  )

  // Empresa/nicho do formulário
  const company = String(contact.companyName || contact.company || formData.empresa || formData.company || '')

  return {
    name:       fullName.trim() || 'Lead sem nome',
    email:      String(contact.email || formData.email || '').trim() || null,
    phone:      String(contact.phone || contact.phoneRaw || formData.telefone || formData.phone || '').trim() || null,
    company:    company || null,
    origem:     mapSource(source),
    status:     'novo',
    operation:  'eua',
    assigned_to: '623dd724-ddeb-426c-956a-4c71f6653fa5',
    assigned_name: 'Lucas',
    notes:      buildNotes(body, formData),
    raw_payload: body,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }
}

function mapSource(src: string): string {
  const s = src.toLowerCase()
  if (s.includes('facebook') || s.includes('fb')) return 'Facebook'
  if (s.includes('instagram') || s.includes('ig')) return 'Instagram'
  if (s.includes('google'))  return 'Google Ads'
  if (s.includes('linkedin')) return 'LinkedIn'
  if (s.includes('indicaç') || s.includes('referral')) return 'Indicação'
  if (s.includes('organic')) return 'Orgânico'
  return 'Magnetic Funnels'
}

function buildNotes(body: Record<string, unknown>, formData: Record<string, unknown>): string {
  const lines: string[] = ['Lead capturado automaticamente via Magnetic Funnels.']
  const type = body.type || body.event_type || ''
  if (type) lines.push(`Evento: ${type}`)
  const extras = Object.entries(formData)
    .filter(([k]) => !['nome','name','email','telefone','phone','empresa','company'].includes(k.toLowerCase()))
    .map(([k, v]) => `${k}: ${v}`)
  if (extras.length) lines.push('Campos extras: ' + extras.join(', '))
  return lines.join('\n')
}

Deno.serve(async (req: Request) => {
  // Preflight CORS
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ ok: false, error: 'Method not allowed' }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 405,
    })
  }

  try {
    const body = await req.json() as Record<string, unknown>

    // Filtra eventos relevantes (form, contact create, lead)
    const type = String(body.type || body.event || body.event_type || 'FormSubmission').toLowerCase()
    const relevant = ['formsubmission', 'contactcreate', 'contact.created', 'form_submission', 'lead']
    const isRelevant = relevant.some(t => type.includes(t)) || !body.type

    if (!isRelevant) {
      return new Response(JSON.stringify({ ok: true, skipped: true, type }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      })
    }

    const leadData = extractContact(body)

    // Usa service role key para bypass de RLS
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
    )

    const { data, error } = await supabase
      .from('leads')
      .insert(leadData)
      .select()
      .single()

    if (error) throw error

    console.log(`[magnetic-webhook] Lead salvo: ${leadData.name} (${leadData.phone})`)

    return new Response(JSON.stringify({ ok: true, lead_id: data.id, name: data.name }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })

  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err)
    console.error('[magnetic-webhook] Erro:', msg)
    return new Response(JSON.stringify({ ok: false, error: msg }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    })
  }
})
