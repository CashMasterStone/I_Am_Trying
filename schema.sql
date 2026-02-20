-- ═══════════════════════════════════════════════════════════════════════════
-- UVT-Stack PostgreSQL Schema — All Four Sites
-- © 2026 Cyrus Makai Schoonover | Born2Build, LLC
-- UTPL™ | SIPL™ | RTPL-BORN2BUILD™
--
-- Run this in Supabase SQL Editor (supabase.com → Project → SQL Editor)
-- ═══════════════════════════════════════════════════════════════════════════

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ══════════════════════════════════════════════════════════════════════════
-- BORN2SUB.COM — Creator Compliance Tables
-- ══════════════════════════════════════════════════════════════════════════

-- Creator onboarding registrations
CREATE TABLE IF NOT EXISTS creator_onboarding (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  legal_name        TEXT NOT NULL,
  email             TEXT NOT NULL UNIQUE,
  platform_type     TEXT DEFAULT 'both',
  jurisdiction      TEXT DEFAULT 'federal',
  content_volume    TEXT,
  wallet_addr       TEXT,
  onboarding_hash   TEXT NOT NULL,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  status            TEXT DEFAULT 'pending_review',
  notes             TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);

-- §2257 Performer records
CREATE TABLE IF NOT EXISTS performer_records (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id           UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  performer_id      TEXT NOT NULL,
  legal_name        TEXT NOT NULL,
  dob               DATE NOT NULL,
  aliases           JSONB DEFAULT '[]',
  document_type     TEXT,
  document_hash     TEXT,   -- SHA256 of the identity document, NOT the document itself
  consent_hash      TEXT,
  consent_date      DATE,
  consent_version   TEXT DEFAULT '1.0',
  compliance_hash   TEXT,
  record_hash       TEXT NOT NULL,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  trace_session_id  UUID,
  merkle_root       TEXT,
  wallet_addr       TEXT,
  platform_id       TEXT DEFAULT 'born2sub-com',
  inspection_ready  BOOLEAN DEFAULT TRUE,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_performer_records_performer_id ON performer_records(performer_id);
CREATE INDEX IF NOT EXISTS idx_performer_records_user_id ON performer_records(user_id);

-- AVOC session audit logs
CREATE TABLE IF NOT EXISTS avoc_sessions (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id        UUID NOT NULL UNIQUE,
  user_id           UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  wallet_addr       TEXT NOT NULL,
  wallet_network    TEXT DEFAULT 'ethereum',
  domain            TEXT NOT NULL,
  consent_hash      TEXT,
  state             TEXT DEFAULT 'TERMINATED',
  audit_log         JSONB DEFAULT '[]',
  trace_log         JSONB DEFAULT '[]',
  merkle_root       TEXT,
  audit_hash        TEXT,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  duration_ms       BIGINT,
  terminated_reason TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  terminated_at     TIMESTAMPTZ
);

-- ══════════════════════════════════════════════════════════════════════════
-- BORN2SUB.TECH — IP Registry & Compliance Query Logs
-- ══════════════════════════════════════════════════════════════════════════

-- IP asset registry
CREATE TABLE IF NOT EXISTS ip_registry (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  asset_name      TEXT NOT NULL,
  asset_type      TEXT NOT NULL,  -- patent | copyright | trademark | trade_secret | nft
  description     TEXT,
  owner_wallet    TEXT,
  asset_hash      TEXT NOT NULL,
  ots_calendar    TEXT,
  ots_proof_hex   TEXT,
  cert            TEXT,
  license         TEXT DEFAULT 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™',
  status          TEXT DEFAULT 'ANCHORED',
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Sovereign query log (AI analysis sessions)
CREATE TABLE IF NOT EXISTS sovereign_queries (
  id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  session_id      UUID,
  query_hash      TEXT NOT NULL,
  domain          TEXT,
  jurisdictions   JSONB DEFAULT '[]',
  query_preview   TEXT,  -- first 100 chars only
  merkle_root     TEXT,
  ots_calendar    TEXT,
  ai_success      BOOLEAN,
  tokens_used     INTEGER,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ══════════════════════════════════════════════════════════════════════════
-- SUPPLY THE SCHOOLS .XYZ — Teacher Requests & Donations
-- ══════════════════════════════════════════════════════════════════════════

-- Classroom supply requests from teachers
CREATE TABLE IF NOT EXISTS school_requests (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  teacher_name      TEXT NOT NULL,
  school_name       TEXT NOT NULL,
  school_email      TEXT NOT NULL,
  grade_level       TEXT,
  state             TEXT,
  student_count     INTEGER,
  description       TEXT NOT NULL,
  supply_categories JSONB DEFAULT '[]',
  estimated_cost    NUMERIC(10, 2),
  funded_amount     NUMERIC(10, 2) DEFAULT 0,
  title_i           BOOLEAN DEFAULT FALSE,
  request_hash      TEXT NOT NULL,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  status            TEXT DEFAULT 'pending_verification',
  -- status options: pending_verification | verified | funded | fulfilled | rejected
  verification_notes TEXT,
  fulfilled_at      TIMESTAMPTZ,
  created_at        TIMESTAMPTZ DEFAULT NOW(),
  updated_at        TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_school_requests_state  ON school_requests(state);
CREATE INDEX IF NOT EXISTS idx_school_requests_status ON school_requests(status);

-- Donations (fiat + crypto)
CREATE TABLE IF NOT EXISTS donations (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stripe_intent_id  TEXT UNIQUE,
  tx_hash           TEXT UNIQUE,
  chain             TEXT,
  amount_cents      INTEGER,
  amount_usd        NUMERIC(10, 2),
  currency          TEXT DEFAULT 'usd',
  donor_email       TEXT,
  from_addr         TEXT,
  request_id        UUID REFERENCES school_requests(id) ON DELETE SET NULL,
  donation_hash     TEXT NOT NULL,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  payment_method    TEXT NOT NULL,  -- stripe | bitcoin | ethereum | solana | base | polygon
  status            TEXT DEFAULT 'completed',
  note              TEXT,
  created_at        TIMESTAMPTZ DEFAULT NOW()
);

-- Increment funded amount on a request (atomic RPC)
CREATE OR REPLACE FUNCTION increment_funded_amount(
  request_id_param   UUID,
  amount_cents_param INTEGER
) RETURNS VOID AS $$
BEGIN
  UPDATE school_requests
  SET
    funded_amount = funded_amount + (amount_cents_param::NUMERIC / 100),
    status = CASE
      WHEN (funded_amount + (amount_cents_param::NUMERIC / 100)) >= estimated_cost THEN 'funded'
      ELSE status
    END,
    updated_at = NOW()
  WHERE id = request_id_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ══════════════════════════════════════════════════════════════════════════
-- SUPPLY THE SCHOOLS DAO — .unstoppable Governance
-- ══════════════════════════════════════════════════════════════════════════

-- DAO Grant Proposals
CREATE TABLE IF NOT EXISTS dao_proposals (
  id                UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  teacher_name      TEXT NOT NULL,
  school_name       TEXT NOT NULL,
  school_email      TEXT NOT NULL,
  state             TEXT,
  student_count     INTEGER,
  description       TEXT NOT NULL,
  amount_needed     NUMERIC(10, 2) NOT NULL,
  wallet_addr       TEXT,
  proposal_hash     TEXT NOT NULL,
  ots_calendar      TEXT,
  ots_proof_hex     TEXT,
  trace_session_id  UUID,
  votes_for         INTEGER DEFAULT 0,
  votes_against     INTEGER DEFAULT 0,
  status            TEXT DEFAULT 'voting_open',
  -- status: voting_open | approved | rejected | fulfilled
  voting_deadline   TIMESTAMPTZ NOT NULL,
  funded_amount     NUMERIC(10, 2) DEFAULT 0,
  cert              TEXT DEFAULT '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922',
  submitted_at      TIMESTAMPTZ DEFAULT NOW(),
  approved_at       TIMESTAMPTZ,
  fulfilled_at      TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_dao_proposals_status   ON dao_proposals(status);
CREATE INDEX IF NOT EXISTS idx_dao_proposals_deadline ON dao_proposals(voting_deadline);

-- DAO vote records (one wallet per proposal, enforced in app layer + here)
CREATE TABLE IF NOT EXISTS dao_votes (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  proposal_id   UUID REFERENCES dao_proposals(id) ON DELETE CASCADE,
  voter_wallet  TEXT NOT NULL,
  vote_direction TEXT NOT NULL CHECK (vote_direction IN ('for', 'against')),
  vote_hash     TEXT NOT NULL,
  ots_calendar  TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(proposal_id, voter_wallet)  -- DB-level idempotency
);
CREATE INDEX IF NOT EXISTS idx_dao_votes_proposal ON dao_votes(proposal_id);

-- DAO impact ledger (on-chain fulfillment records)
CREATE TABLE IF NOT EXISTS dao_ledger (
  id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  proposal_id   UUID REFERENCES dao_proposals(id) ON DELETE SET NULL,
  school_name   TEXT NOT NULL,
  state         TEXT,
  supplies      TEXT,
  amount_usd    NUMERIC(10, 2) NOT NULL,
  tx_hash       TEXT,
  chain         TEXT,
  ledger_hash   TEXT NOT NULL,
  ots_calendar  TEXT,
  ots_proof_hex TEXT,
  fulfilled_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Atomic DAO vote RPC (prevents race conditions)
CREATE OR REPLACE FUNCTION dao_cast_vote(
  proposal_id_param TEXT,
  vote_direction     TEXT,
  voter_wallet       TEXT,
  vote_hash_param    TEXT
) RETURNS JSON AS $$
DECLARE
  updated_proposal RECORD;
BEGIN
  -- Check voting deadline
  IF EXISTS (
    SELECT 1 FROM dao_proposals
    WHERE id = proposal_id_param::UUID AND voting_deadline < NOW()
  ) THEN
    RAISE EXCEPTION 'Voting period has ended for proposal %', proposal_id_param;
  END IF;

  -- Atomic increment
  IF vote_direction = 'for' THEN
    UPDATE dao_proposals
    SET votes_for = votes_for + 1
    WHERE id = proposal_id_param::UUID
    RETURNING * INTO updated_proposal;
  ELSE
    UPDATE dao_proposals
    SET votes_against = votes_against + 1
    WHERE id = proposal_id_param::UUID
    RETURNING * INTO updated_proposal;
  END IF;

  -- Record vote (UNIQUE constraint prevents double-voting at DB level)
  INSERT INTO dao_votes (proposal_id, voter_wallet, vote_direction, vote_hash)
  VALUES (proposal_id_param::UUID, voter_wallet, vote_direction, vote_hash_param);

  RETURN row_to_json(updated_proposal);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ══════════════════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (Supabase RLS)
-- ══════════════════════════════════════════════════════════════════════════

-- Performer records: only owner or service_role can read/write
ALTER TABLE performer_records ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON performer_records
  FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "owner_read" ON performer_records
  FOR SELECT USING (auth.uid() = user_id);

-- Creator onboarding: service_role only
ALTER TABLE creator_onboarding ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_full" ON creator_onboarding
  FOR ALL USING (auth.role() = 'service_role');

-- School requests: public read, service_role write
ALTER TABLE school_requests ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read_verified" ON school_requests
  FOR SELECT USING (status IN ('verified', 'funded', 'fulfilled'));
CREATE POLICY "service_role_full" ON school_requests
  FOR ALL USING (auth.role() = 'service_role');

-- Donations: public insert (for crypto self-reporting), service_role full
ALTER TABLE donations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_insert" ON donations
  FOR INSERT WITH CHECK (true);
CREATE POLICY "service_role_full" ON donations
  FOR ALL USING (auth.role() = 'service_role');

-- DAO proposals: public read + insert, service_role full
ALTER TABLE dao_proposals ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON dao_proposals FOR SELECT USING (true);
CREATE POLICY "public_insert" ON dao_proposals FOR INSERT WITH CHECK (true);
CREATE POLICY "service_role_full" ON dao_proposals FOR ALL USING (auth.role() = 'service_role');

-- DAO votes: public insert (wallet-authenticated), public read
ALTER TABLE dao_votes ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON dao_votes FOR SELECT USING (true);
CREATE POLICY "public_insert" ON dao_votes FOR INSERT WITH CHECK (true);

-- DAO ledger: fully public
ALTER TABLE dao_ledger ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON dao_ledger FOR SELECT USING (true);
CREATE POLICY "service_role_full" ON dao_ledger FOR ALL USING (auth.role() = 'service_role');

-- IP registry: public read
ALTER TABLE ip_registry ENABLE ROW LEVEL SECURITY;
CREATE POLICY "public_read" ON ip_registry FOR SELECT USING (true);
CREATE POLICY "service_role_full" ON ip_registry FOR ALL USING (auth.role() = 'service_role');

-- ══════════════════════════════════════════════════════════════════════════
-- SEED: Pre-populate Born2Build IP Portfolio
-- ══════════════════════════════════════════════════════════════════════════
INSERT INTO ip_registry (asset_name, asset_type, description, license, cert, status) VALUES
  ('MFHST — Meta-Forensic Harvesting Substrate Technology', 'patent', 'Provisional patent filed Oct 16 2025. 14 inventions. Novel substrate for forensic data extraction and provenance anchoring.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('Lumen ISA / Lumen Assembly Language', 'trade_secret', 'Original instruction set architecture. NOT LLVM. Created Sept 2025. Machine-level assembly language with domain-aware opcode sets.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('TRACE Provenance State Machine', 'patent', 'Cert-seeded deterministic state machine. States: 0x0 (SOURCE) → 0x3 (PROCESS) → 0x6 (ALIGN) → 0x9 (LIGHT). Patent pending.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('DSMCALLE Framework', 'patent', 'Domain-Specific Machine Code Assembly Language — 42+ domain-directed assembly DAGs. Novel. No prior art found.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('Zero-True Binary Axiom', 'copyright', '0 = Coherence/Truth; 1 = Collapse/Manifest. Original philosophical-computational axiom. 17 U.S.C. §102.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('ACCCaaS / DomCode ISA', 'copyright', 'Adult Content Creator Compliance as a Service. 18 U.S.C. §2257 automation via DomCode instruction set. Copyright + Patent Pending.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED'),
  ('UTPL™ / SIPL™ / RTPL-BORN2BUILD™', 'trademark', 'Universal Truth Preservation License / Sovereign Innovation Protection License / RTPL-BORN2BUILD. 15 U.S.C. §1051.', 'UTPL™ | SIPL™ | RTPL-BORN2BUILD™', '88BE1B2E·A2ACF1AE·A4A2DC05·1FEAB922', 'ANCHORED')
ON CONFLICT DO NOTHING;

-- ══════════════════════════════════════════════════════════════════════════
-- VERIFY
-- ══════════════════════════════════════════════════════════════════════════
SELECT
  'ip_registry'       AS table_name, COUNT(*) AS rows FROM ip_registry
UNION ALL SELECT
  'creator_onboarding',               COUNT(*) FROM creator_onboarding
UNION ALL SELECT
  'performer_records',                COUNT(*) FROM performer_records
UNION ALL SELECT
  'school_requests',                  COUNT(*) FROM school_requests
UNION ALL SELECT
  'donations',                        COUNT(*) FROM donations
UNION ALL SELECT
  'dao_proposals',                    COUNT(*) FROM dao_proposals
UNION ALL SELECT
  'dao_votes',                        COUNT(*) FROM dao_votes
UNION ALL SELECT
  'dao_ledger',                       COUNT(*) FROM dao_ledger;
