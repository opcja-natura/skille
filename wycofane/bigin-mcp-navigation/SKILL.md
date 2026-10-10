---
name: bigin-mcp-navigation
description: Kompleksowy przewodnik po Zoho Bigin MCP - struktura modułów, relacje, COQL queries, workflow examples, common pitfalls, best practices. Używaj gdy Daniel pyta o strukturę Bigin CRM, potrzebuje pomocy w konstruowaniu zapytań COQL, chce zrozumieć nawigację po rekordach i related lists, szuka przykładów workflow, napotyka błędy w operacjach Bigin lub pyta o ID pracowników w systemie. Zawiera pełną dokumentację 7 modułów głównych (Accounts, Pipelines, Contacts, Products, Tasks, Events, Calls), lookup fields format, CRUD operations, metadata APIs, pagination, bulk operations i dane 6 pracowników z Bigin CRM ID.
---

# Zoho Bigin MCP - Nawigacja i Best Practices

## Kiedy używać tego skilla

Używaj tego skilla gdy Daniel:
- Pyta o strukturę Bigin CRM (moduły, relacje, pola)
- Potrzebuje pomocy w konstruowaniu zapytań COQL
- Chce zrozumieć jak nawigować po rekordach i related lists
- Szuka przykładów workflow i najlepszych praktyk
- Napotyka błędy w operacjach Bigin i potrzebuje troubleshootingu
- Pyta o ID pracowników w systemie Bigin CRM

**Nie używaj** gdy:
- Daniel potrzebuje wykonać konkretną operację (wtedy używaj bezpośrednio narzędzi Bigin MCP)
- Pytanie dotyczy innych systemów niż Bigin CRM

---

## 1. STRUKTURA MODUŁÓW BIGIN

### Moduły główne
- **Accounts** (Firmy/Konta) - główne konta klientów
- **Pipelines** (Deale/Transakcje) - ścieżki sprzedaży, nazywane też "Deals" lub "zamówienia", za zrealizowane uważa się te w etapie "Zamówienie dostarczone"
- **Contacts** (Kontakty) - osoby kontaktowe jeżeli przypisane do firm, lub potencjalni klienci jeżeli kontakt nie ma przypisanej firmy (Accunts)
- **Products** (Produkty) - produkty/usługi
- **Tasks** (Zadania) - zadania do wykonania
- **Events** (Wydarzenia) - spotkania, eventy, nie śledzone w systemie
- **Calls** (Połączenia) - rejestr połączeń, odwołuj się tutaj, jeżeli daniel pyta o aktywność handlowca

### Relacje między modułami
```
Account (Firma)
    ├── Contacts (Kontakty w tej firmie)
    └── Pipelines (Deale związane z firmą)
            ├── Products (Produkty w dealu)
            └── Secondary Contacts (Dodatkowe kontakty)

Contact (Osoba)
    └── Account (Ta strutkrua wskazuje, że jest to kontakt do aktywnego klienta)
    └── brak Account (Ta strutkrua wskazuje, że jest to kontakt potencjalny)

Pipeline (Deal, rozliczenia marketingowe, faktury - przypisane do Account lub Contact)
    ├── Account (Powiązana firma)
    ├── Contact_Name (Główny kontakt)
    ├── Stage (Etap, istotny dla interpretacji)
```

---

## 2. TYPY IDENTYFIKATORÓW I FORMAT DANYCH

### Record ID
- Format: `427926000000297001` (długa liczba)
- Używane w: większości operacji API (get, update, delete)

### API Names modułów
- `Contacts`, `Pipelines`, `Accounts`, `Products`, `Tasks`, `Events`, `Calls`
- **Zawsze** używaj angielskich nazw API, NIE polskich nazw jak "Kontakty"

### Lookup Fields (pola relacyjne)
**KRYTYCZNE:** Lookup fields ZAWSZE mają format obiektu:
```json
{
  "id": "427926000000297001",
  "name": "Nazwa Rekordu"
}
```

**✅ POPRAWNIE:**
```json
{
  "Account_Name": {
    "id": "427926000000640006",
    "name": "Opcja Natura"
  }
}
```

**❌ BŁĄD - NIE UŻYWAJ:**
```json
{
  "Account_Name": "427926000000640006"  // STRING - nie zadziała!
}
```

### Checkbox Fields
- **Checked**: `"__YES__"`
- **Unchecked**: `"__NO__"`

### Date Fields
Proste pola dat: format `YYYY-MM-DD`
```json
{
  "Due_Date": "2024-12-25"
}
```

Rozszerzone pola dat (np. w create-pages):
```json
{
  "date:Due Date:start": "2024-12-25",
  "date:Due Date:end": "2024-12-31",
  "date:Due Date:is_datetime": 0
}
```

---

## 3. PODSTAWOWE OPERACJE

### Search Records (wyszukiwanie)
**Parametr `criteria`:**
```
(({field_api_name}:{comparator}:{value}))
```

**Przykłady:**
```
// Email equals
((Email:equals:john@example.com))

// Multiple conditions
((Last_Name:equals:Smith)and(Email:equals:john@example.com))

// NOT operator
(not(Stage:equals:Closed Won))

// IN operator dla małych list (<10 elementów)
((Status:in:Active,Pending,New))
```

**Komparatory według typu danych:**
- **Text/Email/Phone**: `equals`, `not_equal`, `starts_with`, `in`
- **Number/Currency**: `equals`, `not_equal`, `greater_than`, `greater_equal`, `less_than`, `less_equal`, `between`, `in`
- **Date**: `equals`, `not_equal`, `greater_than`, `greater_equal`, `less_than`, `less_equal`, `between`
- **Boolean**: `equals`, `not_equal`, `in`

### Get Specific Record
```
Bigin_getSpecificRecord({
  module_api_name: "Contacts",
  id: "427926000000297001"
})
```

### COQL Queries (zaawansowane zapytania)
Format: SQL-like SELECT statement
```sql
SELECT Last_Name, Email, Account_Name 
FROM Contacts 
WHERE Stage = 'Qualified'
ORDER BY Created_Time DESC 
LIMIT 200
```

**Ograniczenia COQL:**
- Brak JOIN - używaj lookup fields zamiast tego
- MAX 200 rekordów w jednym zapytaniu
- Brak GROUP BY - używaj narzędzia `Bigin_getRecords` z agregacjami
- Dla dużych list (>10 elementów) używaj IN z podzapytaniem:
  ```sql
  WHERE Owner IN (SELECT id FROM Users WHERE name = 'Łukasz')
  ```

---

## 4. PIPELINE OPERATIONS

### Team Pipelines vs Sub-Pipelines
- **Team Pipeline** (Pipeline) - główna kategoria (np. "Sprzedaż", "Customer Support")
- **Sub-Pipeline** - podkategoria w ramach Team Pipeline (np. "Q1 2024", "Reklamacje")


### Stages (Etapy)
Stage MUSI pasować do wybranego Pipeline/Sub-Pipeline. Sprawdź dostępne etapy przez:
```
Bigin_getLayoutsMetadata({ module: "Pipelines" })
```

---

## 5. METADATA (POZNAWANIE STRUKTURY)

### Moduły w systemie
```
Bigin_getModules()
```
Zwraca listę wszystkich modułów i ich podstawowe właściwości.

### Layouts (Struktury formularzy)
```
Bigin_getLayoutsMetadata({ module: "Pipelines" })
```
Zawiera:
- Dostępne Team Pipelines (layouts)
- Stages dla każdego pipeline
- Pola wymagane w każdym layout

### Fields (Szczegóły pól)
NIE MA dedykowanego narzędzia `getFields` - używaj:
```
Bigin_getLayoutsMetadata({ module: "Contacts" })
```
W response w sekcji `sections` → `fields` znajdziesz wszystkie pola.

### Related Lists (Powiązane rekordy)
```
Bigin_getRelatedListsMetadata({ module: "Accounts" })
```
Zwraca listę dostępnych related lists dla modułu (np. Contacts, Deals dla Account).

### Custom Views (Widoki)
```
Bigin_getCustomViewsMetadata({ module: "Pipelines" })
```
Lista zapisanych filtrów/widoków.

---

## 6. CRUD OPERATIONS

### CREATE (Tworzenie rekordów)
```json
Bigin_addRecords({
  module_api_name: "Contacts",
  body: {
    data: [
      {
        "Last_Name": "Kowalski",
        "Email": "jan.kowalski@example.com",
        "Account_Name": {
          "id": "427926000000640006",
          "name": "Opcja Natura"
        }
      }
    ]
  }
})
```

### UPDATE (Aktualizacja rekordów)
```json
Bigin_updateRecords({
  module_api_name: "Contacts",
  body: {
    data: [
      {
        "id": "427926000000297001",
        "Email": "nowy.email@example.com",
        "Mobile": "+48123456789"
      }
    ]
  }
})
```

### DELETE (Usuwanie przez zmianę owner)
Bigin nie ma bezpośredniego DELETE - używaj:
```
Bigin_changeMultipleRecordOwners()
```
lub archive przez zmianę statusu.

---

## 7. WORKFLOW EXAMPLES

### Przykład 1: Znajdź wszystkie zamówienia dla klienta "ABC Corp"
```sql
SELECT Deal_Name, Amount, Stage, Closing_Date 
FROM Pipelines 
WHERE Account_Name = 'ABC Corp' 
ORDER BY Closing_Date DESC
```

### Przykład 2: Znajdź klientów bez zamówień od 180+ dni
**Krok 1:** Znajdź klientów z ostatnim zamówieniem
```sql
SELECT Account_Name, MAX(Closing_Date) as Last_Order 
FROM Pipelines 
WHERE Stage = 'Closed Won' 
GROUP BY Account_Name
```

**Krok 2:** Filtruj w Python/JS po dacie (COQL nie wspiera DATE_DIFF)

### Przykład 3: Zaktualizuj owner dla wielu rekordów
```json
Bigin_changeMultipleRecordOwners({
  module_api_name: "Pipelines",
  body: {
    "ids": ["427926000001782001", "427926000001782002"],
    "owner": {
      "id": "427926000000706904"
    },
    "notify": true
  }
})
```

---

## 8. COMMON PITFALLS (Najczęstsze błędy)

### ❌ Błąd 1: Używanie polskich nazw modułów
```
// BŁĄD:
module_api_name: "Kontakty"

// POPRAWNIE:
module_api_name: "Contacts"
```

### ❌ Błąd 2: Lookup field jako string
```json
// BŁĄD:
{
  "Account_Name": "427926000000640006"
}

// POPRAWNIE:
{
  "Account_Name": {
    "id": "427926000000640006",
    "name": "Opcja Natura"
  }
}
```

### ❌ Błąd 3: Brak paginacji
Bigin zwraca MAX 200 rekordów per request. Dla większych zbiorów:
```
page=1, per_page=200  // pierwsze 200
page=2, per_page=200  // kolejne 200
```

### ❌ Błąd 4: COQL IN operator dla dużych list
```sql
-- BŁĄD (wolne dla >10 elementów):
WHERE Owner IN ('id1', 'id2', 'id3', ..., 'id100')

-- POPRAWNIE (szybkie):
WHERE Owner IN (
  SELECT id FROM Users WHERE Team = 'Sales'
)
```

### ❌ Błąd 5: Nie sprawdzenie Related Lists przed użyciem
```
// NAJPIERW sprawdź co jest dostępne:
Bigin_getRelatedListsMetadata({ module: "Tasks" })

// POTEM dopiero pobieraj:
Bigin_getRelatedListRecords({
  module_api_name: "Tasks",
  id: "...",
  related_list_api_name: "Notes"  // sprawdzone że istnieje
})
```

---

## 9. BEST PRACTICES

### 1. Zawsze używaj COQL dla complex queries
Zamiast wielu wywołań `getRecords` z różnymi filtrami, użyj jednego COQL:
```sql
SELECT Account_Name, Deal_Name, Amount, Stage 
FROM Pipelines 
WHERE (Stage = 'Qualification' OR Stage = 'Proposal') 
  AND Amount > 10000 
  AND Owner = '427926000000706904'
ORDER BY Amount DESC 
LIMIT 200
```

### 2. Batch operations zamiast pojedynczych
```json
// DOBRZE - 1 request, 100 rekordów:
Bigin_addRecords({
  body: {
    data: [/* 100 rekordów */]
  }
})

// ŹLE - 100 requestów:
for (contact in contacts) {
  Bigin_addRecords({ data: [contact] })
}
```

### 3. Minimalizuj wywołania API
- Cache metadata (layouts, fields) - zmieniają się rzadko
- Używaj `fields` parameter żeby pobierać tylko potrzebne pola
- Limit pagination do minimum (per_page=200 max)

### 4. Error handling
```javascript
try {
  const result = await Bigin_getSpecificRecord({...});
  // handle success
} catch (error) {
  if (error.code === 'INVALID_MODULE') {
    // sprawdź nazwę modułu
  } else if (error.code === 'RECORD_NOT_FOUND') {
    // rekord nie istnieje
  }
}
```

### 5. Zawsze weryfikuj lookup IDs
Przed utworzeniem/aktualizacją rekordu z lookup field, sprawdź czy ID istnieje:
```
Bigin_getSpecificRecord({
  module_api_name: "Accounts",
  id: "427926000000640006"
})
```

---

## 10. QUICK REFERENCE CHEATSHEET

### Podstawowe operacje
```
Lista rekordów:     Bigin_getRecords
Pojedynczy rekord:  Bigin_getSpecificRecord
Szukaj:            Bigin_searchRecords
COQL query:        Bigin_getRecordsUsingCoqlQuery
Utwórz:            Bigin_addRecords
Aktualizuj:        Bigin_updateRecords / updateSpecificRecord
```

### Metadata
```
Moduły:            Bigin_getModules
Layouts:           Bigin_getLayoutsMetadata
Related Lists:     Bigin_getRelatedListsMetadata
Custom Views:      Bigin_getCustomViewsMetadata
```

### Related Records
```
Pobierz:           Bigin_getRelatedListRecords
Aktualizuj:        Bigin_updateRelatedListRecords
```

### Notatki i tagi
```
Notatki:           Bigin_getNotes / addNotesToSpecificRecord
Tagi:              Bigin_getTags / addTagsToSpecificRecord
```

### Użytkownicy
```
Zmiana owner:      Bigin_changeMultipleRecordOwners
```

---

## 11. BULK OPERATIONS

### Bulk Read (Export danych)
```json
Bigin_createBulkRead({
  body: {
    "query": {
      "module": "Contacts",
      "fields": ["Last_Name", "Email", "Created_Time"],
      "criteria": {
        "group": [
          {
            "api_name": "Created_Time",
            "comparator": "greater_equal",
            "value": "2024-01-01T00:00:00+01:00"
          }
        ],
        "group_operator": "and"
      }
    },
    "callback": {
      "url": "https://your-webhook.com/callback",
      "method": "post"
    },
    "file_type": "csv"
  }
})
```

### Bulk Write (Import danych)
**Krok 1:** Upload pliku
**Krok 2:** Stwórz bulk write job
```json
Bigin_createBulkWriteJob({
  body: {
    "operation": "insert",
    "resource": [
      {
        "type": "data",
        "module": { "api_name": "Contacts" },
        "file_id": "uploaded_file_id",
        "field_mappings": [
          { "api_name": "Last_Name", "index": 0 },
          { "api_name": "Email", "index": 1 }
        ]
      }
    ]
  }
})
```

---

## 12. PRACOWNICY Z DOSTĘPEM DO BIGIN CRM

### 6 pracowników z Bigin CRM ID:

1. **Daniel Suliga** (CEO)
   - Bigin ID: `427926000000297001`
   - Email: daniel@opcjanatura.pl
   - Tel: 790472352
   - Slack: U01EM50N9ML

2. **Krystian Konieczny** (E-commerce Manager)
   - Bigin ID: `427926000000640006`
   - Email: krystian@opcjanatura.pl
   - Tel: 536214728
   - Slack: U08QRU291V2

3. **Łukasz Jakubiec** (Handlowiec)
   - Bigin ID: `427926000000706904`
   - Email: lukasz@opcjanatura.pl
   - Tel: 534872433
   - Slack: U08MAEU4KKJ

4. **Konrad Orzechowski** (Handlowiec)
   - Bigin ID: `427926000001433004`
   - Email: konrad@opcjanatura.pl
   - Tel: 537042165
   - Slack: U08TF8DSQS1

5. **Monika Kwiecień-Gonda** (Export Manager)
   - Bigin ID: `427926000001535630`
   - Email: export@opcjanatura.pl
   - Tel: 533420798
   - Slack: U0ACBMY3H8W

6. **Grzegorz Gęsiarek** (Dyrektor Handlowy)
   - Bigin ID: `427926000000720544`
   - Tel: 669536055
   - Slack: U08M5CL8L68

### Przykłady użycia:

**Filtrowanie po Owner (COQL):**
```sql
SELECT Deal_Name, Amount, Stage 
FROM Pipelines 
WHERE Owner = '427926000000706904'  -- Łukasz
ORDER BY Created_Time DESC
```

**Zmiana właściciela rekordów:**
```json
Bigin_changeMultipleRecordOwners({
  module_api_name: "Pipelines",
  body: {
    "ids": ["427926000001782001"],
    "owner": {
      "id": "427926000001535630"  // Monika
    }
  }
})
```

**Tworzenie rekordu z właścicielem:**
```json
{
  "Deal_Name": "Nowy deal",
  "Owner": {
    "id": "427926000000706904",  // Łukasz
    "name": "Łukasz Jakubiec"
  }
}
```
