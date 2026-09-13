CREATE TABLE bronze_purchases__credit_approved (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  installments INTEGER,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_denied (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  denial_reason TEXT NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_cancelled (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  cancellation_reason TEXT,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_clearing (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_processed (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  network_fee REAL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__debit_approved (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__debit_denied (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  denial_reason TEXT NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__debit_cancelled (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  cancellation_reason TEXT,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__debit_clearing (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__debit_processed (
  event_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  status TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  network_fee REAL,
  event_timestamp TEXT NOT NULL,
  ingest_timestamp TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_transaction (
  transaction_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  installment_number INTEGER NOT NULL,
  installment_amount REAL NOT NULL,
  installment_interest_rate REAL,
  transaction_type_id TEXT NOT NULL
);

CREATE TABLE bronze_purchases__credit_transaction_type (
  transaction_type_id TEXT NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE silver_l1_purchases__credit_purchase (
  purchase_id TEXT NOT NULL,
  event_sequence INTEGER NOT NULL,
  status TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  processed_timestamp TEXT NOT NULL
);

CREATE TABLE silver_l1_purchases__debit_purchase (
  purchase_id TEXT NOT NULL,
  event_sequence INTEGER NOT NULL,
  status TEXT NOT NULL,
  event_timestamp TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  processed_timestamp TEXT NOT NULL
);

CREATE TABLE silver_l2_purchases__credit_purchase (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  status TEXT NOT NULL,
  status_timestamp TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_count INTEGER NOT NULL
);

CREATE TABLE silver_l2_purchases__debit_purchase (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  status TEXT NOT NULL,
  status_timestamp TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  event_count INTEGER NOT NULL
);

CREATE TABLE silver_purchases__credit_transaction (
  transaction_id TEXT NOT NULL PRIMARY KEY,
  purchase_id TEXT NOT NULL,
  installment_number INTEGER NOT NULL,
  installment_amount REAL NOT NULL,
  installment_interest_rate REAL,
  transaction_type_id TEXT NOT NULL
);

CREATE TABLE silver_purchases__credit_transaction_type (
  transaction_type_id TEXT NOT NULL PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE gold_integration__purchase_journey (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  rail TEXT NOT NULL,
  status TEXT NOT NULL,
  status_timestamp TEXT NOT NULL,
  card_id TEXT NOT NULL,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  merchant_id TEXT NOT NULL,
  merchant_category_code TEXT NOT NULL,
  channel TEXT NOT NULL,
  installments INTEGER,
  reversal_amount REAL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE gold_analytics__extrato_cliente (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  customer_id TEXT NOT NULL,
  amount REAL NOT NULL,
  status TEXT NOT NULL,
  transaction_date TEXT NOT NULL,
  merchant_name TEXT
);

CREATE TABLE gold_analytics__comportamento_gasto (
  customer_id TEXT NOT NULL PRIMARY KEY,
  total_spent REAL NOT NULL,
  average_ticket REAL NOT NULL,
  purchase_count INTEGER NOT NULL,
  top_category TEXT
);

CREATE TABLE gold_analytics__taxa_aprovacao_compra (
  periodo TEXT NOT NULL,
  segmento TEXT NOT NULL,
  total_compras INTEGER NOT NULL,
  compras_aprovadas INTEGER NOT NULL,
  compras_negadas INTEGER NOT NULL,
  taxa_aprovacao REAL NOT NULL,
  PRIMARY KEY (periodo, segmento)
);

CREATE TABLE gold_analytics__motivos_negacao_compra (
  denial_reason TEXT NOT NULL PRIMARY KEY,
  count INTEGER NOT NULL,
  percentage REAL NOT NULL
);

CREATE TABLE gold_analytics__ranking_lojista_categoria (
  merchant_category_code TEXT NOT NULL PRIMARY KEY,
  merchant_name TEXT,
  count INTEGER NOT NULL,
  total_spent REAL NOT NULL
);

CREATE TABLE gold_analytics__adocao_parcelamento (
  installment_count INTEGER NOT NULL PRIMARY KEY,
  total_compras INTEGER NOT NULL,
  average_amount REAL NOT NULL,
  percentage REAL NOT NULL
);

CREATE TABLE gold_analytics__latencia_liquidacao_compra (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  approved_timestamp TEXT NOT NULL,
  clearing_timestamp TEXT,
  processed_timestamp TEXT NOT NULL,
  latencia_minutos INTEGER NOT NULL
);

CREATE TABLE gold_analytics__mix_canal (
  channel TEXT NOT NULL PRIMARY KEY,
  count INTEGER NOT NULL,
  percentage REAL NOT NULL
);

CREATE TABLE gold_analytics__gasto_internacional (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  amount_usd REAL NOT NULL,
  amount_brl REAL NOT NULL,
  exchange_rate REAL NOT NULL
);

CREATE TABLE gold_analytics__gasto_elegivel_rewards (
  purchase_id TEXT NOT NULL PRIMARY KEY,
  customer_id TEXT NOT NULL,
  eligible_amount REAL NOT NULL,
  category TEXT NOT NULL
);