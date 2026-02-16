# Adding New RA Templates

This guide explains the complete process of adding a new PDF template to the RA Automator so that the **Generate RA** flow shows the right form fields and fills the PDF correctly.

---

## Overview

When you add a new template:

1. **Place the PDF** in the templates folder (no code change).
2. **Add frontend logic** so the form shows/hides the correct fields for that template name.
3. **Backend**: Usually no change—existing fields (client name, subject property, advance fee, flat fee, attorney, schedule) are already supported. Only if your template uses a **new** placeholder do you add backend + form support for it.

---

## 1. Where Templates Live

- **Folder:** `public/RA_Templates/`
- **Add your PDF** there (e.g. `My-New-Template.pdf`).
- The app lists all `.pdf` files in this folder via the API; no code change is needed to “register” a new file.

**Backend listing** (for reference only; you don’t edit this when adding a template):

- **File:** `backend/routes.py`
- **Endpoint:** `GET /api/ra-templates`
- **Logic:** Scans `project_root / "public" / "RA_Templates"`, returns `{ name, path }` for each file.

---

## 2. PDF Placeholder Format

The PDF filler looks for placeholders in this form:

```text
{{variable_name}}
```

Examples:

- `{{client.name}}` or `{{Client Name}}` or `{{clientName}}`
- `{{Subject Property}}` or `{{subject_property}}`
- `{{Advance}}` or `{{Advance Fee Deposit}}`
- `{{flat_fee}}` or `{{Flat Fee}}`
- `{{attorney}}` or `{{Attorney}}`
- `{{schedule}}` or `{{Schedule}}`

Nested keys like `{{client.name}}` are supported; the backend maps form values to multiple key variants so common names work.

---

## 3. Supported Form Fields (No Backend Change Needed)

These are already in the backend and in the form. Your job is only to **show/hide** the right ones for your template.

| Form field           | Backend key(s) used in PDF fill      | Used for templates that need |
|----------------------|--------------------------------------|------------------------------|
| Client Name          | `client.name`, `clientName`, `Client Name` | Client name                  |
| Subject Property     | `subject_property`, `Subject Property`, `SubjectProperty` | Property address             |
| Advance Fee Deposit  | `Advance`, `Advance Fee Deposit`, `AdvanceFeeDeposit` | Advance fee (number → e.g. $1,234.00) |
| Flat Fee             | `flat_fee`, `flatFee`, `Flat Fee`, `FlatFee` | Flat fee (number → e.g. $500.00) |
| Attorney             | `attorney`, `Attorney`, `attorney.name` | Attorney name                |
| Schedule             | `schedule`, `Schedule`               | Schedule text                |
| Output File Name     | (used for file name only)            | Every template               |

If your template **only** uses placeholders that match the table above, you **do not** change the backend. You only add one block in the frontend (Step 4).

---

## 4. Frontend: Show the Right Form for Your Template

**File:** `public/dashboard.html`

**Function:** `selectTemplate(template, element)` — inside it there is a long `if / else if / else` chain that runs when a user clicks a template. Each branch matches a template **by name** (lowercased) and then shows/hides field groups.

### 4.1 Template name matching

- The name used for matching is **the file name, lowercased**, e.g. `my-new-template.pdf`.
- Use `templateName.includes('some-unique-part')` so you don’t accidentally match other templates.
- Put more specific templates **higher** in the chain so they match before generic ones.

### 4.2 Field group IDs (use these in your new block)

| What you want in the form | Element ID                    | Action in code                          |
|---------------------------|-------------------------------|----------------------------------------|
| Output File Name          | (always visible)              | No change                              |
| Client Name               | `clientNameFieldGroup`        | `classList.remove('hidden')` + set `required` |
| Subject Property          | `subjectPropertyFieldGroup`   | same                                   |
| Advance Fee Deposit       | `advanceFeeDepositFieldGroup` | same                                   |
| Flat Fee                  | `flatFeeFieldGroup`           | same                                   |
| Attorney                  | `attorneyFieldGroup`          | same                                   |
| Schedule                  | `scheduleFieldGroup`          | same                                   |

For fields you **don’t** want for this template:

- `fieldGroup.classList.add('hidden')`
- `input.removeAttribute('required')`
- `input.value = ''`

Use the same variable names as in the existing blocks:  
`clientNameFieldGroup`, `clientNameInput`, `subjectPropertyFieldGroup`, `subjectPropertyInput`, `advanceFeeDepositFieldGroup`, `advanceFeeDepositInput`, `flatFeeFieldGroup`, `flatFeeInput`, `attorneyFieldGroup`, `attorneyInput`, `scheduleFieldGroup`, `scheduleInput`.

### 4.3 Where to add your block

Add a **new `else if`** in the same chain, in a place that makes sense for your template name (so more specific names are above more generic ones). Do **not** put it inside the ADDENDUM block (that one uses `return` and shows the form itself).

**Example:** Template **“AA2-CA-LOSS MIT”** needs: Client Name, Subject Property, Attorney, Flat Fee.

Add this **after** the “AA2-CA-ProSe and Loss Mit” block and **before** the “AA2-HOA-RA-complete” block:

```javascript
// Template: "AA2-CA-LOSS MIT" (note space in "LOSS MIT")
// Fields: clientName, subjectProperty, attorney, flat_fee
else if (templateName.includes('aa2-ca-loss mit')) {
    // Show client, subject, attorney and flat fee, hide advance fee deposit and schedule
    clientNameFieldGroup.classList.remove('hidden');
    clientNameInput.setAttribute('required', 'required');
    subjectPropertyFieldGroup.classList.remove('hidden');
    subjectPropertyInput.setAttribute('required', 'required');
    attorneyFieldGroup.classList.remove('hidden');
    attorneyInput.setAttribute('required', 'required');
    flatFeeFieldGroup.classList.remove('hidden');
    flatFeeInput.setAttribute('required', 'required');
    scheduleFieldGroup.classList.add('hidden');
    scheduleInput.removeAttribute('required');
    scheduleInput.value = '';
    advanceFeeDepositFieldGroup.classList.add('hidden');
    advanceFeeDepositInput.removeAttribute('required');
    advanceFeeDepositInput.value = '';
}
```

### 4.4 Special case: ADDENDUM-style (only client + schedule)

If your template should show **only** Client Name and Schedule (like ADDENDUM-CA-LOSSMIT), the logic is already in an **`if`** block that also **shows the form** and **returns**. Do not duplicate that block; add a similar **`else if`** only if you have another template that needs the same set of fields. For a single “client + schedule only” template, the existing ADDENDUM block is the pattern.

### 4.5 Order of conditions

Rough order used in the app (keep this in mind so your new template matches first when it should):

1. ADDENDUM-CA-LOSSMIT (client + schedule only; has `return` and shows form inside block).
2. Payment Authorization (output-only).
3. AA2-CA-ProSe and Loss Mit.
4. **Your new template (e.g. AA2-CA-LOSS MIT).**
5. AA2-HOA-RA-complete, AA2-PRIVATELIEN, AA2-LOSSMIT variants, AA2-FULLSERVICE-FINAL.
6. Final `else` (default: client, subject, advance, attorney).

---

## 5. Form Submit and Back to Templates

- **Form submit** (`generateRaForm` submit handler) already sends only **visible** fields: it checks each field group’s `classList.contains('hidden')` and only includes `clientName`, `subjectProperty`, `advanceFeeDeposit`, `flatFee`, `attorney`, or `schedule` if the corresponding group is not hidden.
- **Back to Templates** (`backToTemplates`) resets to the default set of visible fields (e.g. client, subject, advance) and hides attorney, flat fee, schedule. You don’t need to change this when adding a new template that uses only the existing fields.

So: **for a new template that only uses the existing six fields, you only add the one `else if` block in `selectTemplate()`.**

---

## 6. Adding a Brand‑New Field (Rare)

Only do this if your PDF has a placeholder that is **not** one of: client name, subject property, advance fee, flat fee, attorney, schedule.

1. **Backend – request model**  
   **File:** `backend/routes.py`  
   In `GenerateRARequest`, add a new optional field, e.g. `myNewField: str = None`.

2. **Backend – data mapping**  
   In `generate_ra`, in the block where `data = {}` is built, add something like:
   ```python
   if request.myNewField:
       data["my_new_field"] = request.myNewField
       data["My New Field"] = request.myNewField  # add any variants your PDF uses
   ```

3. **Frontend – HTML**  
   In `public/dashboard.html`, in the Generate RA form section, add a new field group (same structure as the existing ones), with a unique ID, e.g. `id="myNewFieldFieldGroup"` and `id="myNewField"`, and give the group `class="form-group hidden"` so it’s hidden by default.

4. **Frontend – `selectTemplate()`**  
   In your new template’s `else if` block, show the new group:  
   `document.getElementById('myNewFieldFieldGroup').classList.remove('hidden');`  
   and set `required` if needed; in other templates, add `myNewFieldFieldGroup` to the list of groups you hide and clear.

5. **Frontend – form submit**  
   In the submit handler, add a check: if `!myNewFieldFieldGroup.classList.contains('hidden')`, then `formData.myNewField = document.getElementById('myNewField').value` (or equivalent).

6. **Frontend – `backToTemplates()`**  
   Reset the new field: hide `myNewFieldFieldGroup`, clear and remove `required` from `myNewField`.

7. **PDF**  
   Use a placeholder like `{{my_new_field}}` or `{{My New Field}}` in the PDF so it matches the keys you put in `data`.

---

## 7. Quick Checklist (Existing Fields Only)

- [ ] Put the PDF in `public/RA_Templates/`.
- [ ] In `public/dashboard.html`, in `selectTemplate()`, add one `else if` that:
  - Matches your template name with `templateName.includes('...')` (lowercased, unique substring).
  - Shows the field groups you need (`classList.remove('hidden')`, set `required` where needed).
  - Hides the rest (`classList.add('hidden')`, `removeAttribute('required')`, `value = ''`).
- [ ] Place the block so it doesn’t get overridden by a more generic condition (order in the if/else if chain).
- [ ] Confirm your PDF uses only placeholders that match the supported keys (see table in Section 3).

No backend or form-structure change is required when using only the six existing fields.

---

## 8. Reference: Backend Data Keys (routes.py)

So you can match your PDF placeholders to what the app sends:

| Request field       | Keys set in `data` (sample) |
|---------------------|-----------------------------|
| `clientName`         | `client.name`, `clientName`, `Client Name`, `client` → `{ name }` |
| `subjectProperty`    | `subject_property`, `Subject Property`, `SubjectProperty` |
| `advanceFeeDeposit` | `Advance`, `Advance Fee Deposit`, `AdvanceFeeDeposit` (formatted as $) |
| `flatFee`           | `flat_fee`, `flatFee`, `Flat Fee`, `FlatFee` (formatted as $) |
| `attorney`          | `attorney`, `Attorney`, `attorney.name` |
| `schedule`          | `schedule`, `Schedule` |

The filler also supports nested keys (e.g. `client.name`) via `get_value_from_data()` in `backend/routes.py`.
