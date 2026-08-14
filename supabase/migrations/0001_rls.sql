-- ============================================================================
-- SoroMais — Row Level Security policies
-- Run in Supabase: SQL Editor (or store in supabase/migrations and apply via
-- the CLI). After applying, test from outside the backend with curl using the
-- anon key to confirm denial of writes, e.g.:
--   curl -X POST "$SUPABASE_URL/rest/v1/paciente" \
--     -H "apikey: $ANON_KEY" -H "Authorization: Bearer $ANON_KEY" \
--     -H "Content-Type: application/json" -d '{"nome_do_paciente":"x"}'
-- Expect: 401/403 (RLS denies anon writes).
-- ============================================================================

-- 1) Turn RLS ON for every table that holds data.
alter table if exists hospital enable row level security;
alter table if exists paciente enable row level security;
alter table if exists local   enable row level security;

-- 2) hospital: public read-only list (the app fetches hospitals through the API).
--    Anonymous callers may SELECT; they must NOT insert/update/delete.
drop policy if exists hospital_select_anon on hospital;
create policy hospital_select_anon on hospital
  for select to anon
  using (true);

-- 3) paciente / local: contain PII and are written by the backend.
--    Writes are allowed ONLY for the service_role (server secret). The anon key
--    can read (so the API can return what it just inserted) but cannot write.
--    This is the core "enforce via RLS, not key secrecy" control.
drop policy if exists paciente_select_anon on paciente;
create policy paciente_select_anon on paciente
  for select to anon
  using (true);

drop policy if exists paciente_write_service on paciente;
create policy paciente_write_service on paciente
  for insert to service_role
  with check (true);

drop policy if exists local_select_anon on local;
create policy local_select_anon on local
  for select to anon
  using (true);

drop policy if exists local_write_service on local;
create policy local_write_service on local
  for insert to service_role
  with check (true);

-- ----------------------------------------------------------------------------
-- ALTERNATIVE (anon-only backend): if you deliberately run the backend with the
-- anon key and refuse to use service_role anywhere, replace the *_write_service
-- policies above with anon-writing policies, e.g.:
--
--   create policy paciente_write_anon on paciente
--     for insert to anon with check (true);
--
-- WARNING: with anon-writing policies, anyone who extracts the (public) anon key
-- can write directly to your DB. The API-key gate in front of the backend then
-- becomes your only protection, so keep API_KEY/JWT_SECRET enforced in prod.
-- The service_role + RLS approach above is preferred.
-- ----------------------------------------------------------------------------
