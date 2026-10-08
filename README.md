# BCO-DMO submission tool: LLM quick prompts

This repository holds the **Quick Prompts** shown on the LLM page of a dataset
submission in the submission tool. The submission API reads it from the
`main` branch, so editing it here changes the prompts data managers see,
without a code deployment. The repository is public on purpose: the API reads
it with no credential, so there is no token that can expire. Don't put
anything in here that shouldn't be public.

Two kinds of files:

- `quick-prompts.json` lists the prompts: their order, ids, labels and options.
- `prompts/<id>.txt` holds the text of each prompt, one file per prompt,
  named after the prompt's `id`. Write it like a plain text document; blank
  lines, paragraphs and lists are passed to the LLM as they are.

## Making a change

1. To change a prompt's wording, edit `prompts/<id>.txt`. To add a prompt,
   add an entry to `quick-prompts.json` and create `prompts/<id>.txt`. To
   remove one, delete both.
2. Push or merge to `main` (editing on GitHub directly works fine).
3. In the submission tool, open any submission, then **DM Actions → Refresh
   Quick Prompts**. The API caches the files and only re-reads them on a new
   deployment or when that button is pressed.

If the files fail the checks below, the API keeps serving the previous prompts
and the refresh button shows the error, so a mistake never leaves the LLM page
without prompts. The `Validate` GitHub Action runs the same checks on every
push, so look at the Actions tab if a refresh reports a problem.

## quick-prompts.json

```json
{
  "quickPrompts": [
    {
      "id": "extract_timezone",
      "label": "Extract Timezone",
      "icon": "calendar",
      "includePublications": false,
      "includePeople": false,
      "includeChecklist": false,
      "includeRedmineTicket": false,
      "fileSelection": "none"
    }
  ]
}
```

Prompts appear in the order they are listed.

| Field                 | Required | Meaning                                                                                                                                                                                                                         |
| --------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                  | yes      | Unique, stable identifier: lowercase letters, numbers and underscores. The prompt text is read from `prompts/<id>.txt`. It is recorded with every LLM conversation and in usage reporting, so **keep an existing id when editing its prompt**, and pick a new id for a new prompt. |
| `label`               | yes      | Text shown on the button.                                                                                                                                                                                                     |
| `icon`                | no       | Icon next to the label, one of the names listed below. Leave it out for no icon. An unknown name also shows no icon.                                                                                                           |
| `includePublications` | no       | `true` or `false` ticks or unticks the "Include publications" option when the prompt is chosen. Leave it out to keep whatever the user had set.                                                                                   |
| `includePeople`       | no       | Same for "Include people".                                                                                                                                                                                                    |
| `includeChecklist`    | no       | Same for "Include checklist".                                                                                                                                                                                                 |
| `includeRedmineTicket`| no       | Same for "Include Redmine ticket".                                                                                                                                                                                            |
| `fileSelection`       | no       | What happens to the "Files" selection when the prompt is chosen: `none` clears it (default), `parameterFiles` selects every data file that has parameters defined, `keep` leaves it alone.                                        |

## Icons

These are the values the `icon` field accepts (Font Awesome solid icons):


`book`, `book-open`, `newspaper`, `quote-left`, `link`, `tag`, `tags`, `bookmark`, `flag`, `star`, `file`, `file-lines`, `file-csv`, `file-excel`, `file-code`, `folder`, `database`, `table`, `table-columns`, `table-list`, `columns`, `list`, `list-check`, `clipboard-list`, `clipboard-check`, `align-left`, `hashtag`, `search`, `magnifying-glass`, `filter`, `sort`, `eye`, `lightbulb`, `question-circle`, `info-circle`, `exclamation-triangle`, `check`, `check-double`, `user`, `users`, `id-card`, `address-book`, `envelope`, `building`, `university`, `graduation-cap`, `calendar`, `calendar-days`, `calendar-check`, `clock`, `stopwatch`, `hourglass`, `history`, `map`, `location-dot`, `compass`, `globe`, `earth-americas`, `satellite`, `mountain`, `ship`, `anchor`, `water`, `droplet`, `fish`, `bug`, `leaf`, `tree`, `seedling`, `paw`, `cow`, `wind`, `cloud`, `sun`, `snowflake`, `thermometer-half`, `flask`, `vial`, `dna`, `microscope`, `atom`, `chart-line`, `chart-bar`, `calculator`, `square-root-variable`, `percent`, `ruler`, `weight-scale`, `scale-balanced`, `cogs`, `code`, `robot`, `brain`, `wand-magic-sparkles`, `bolt`, `language`, `spell-check`, `comments`, `pen`, `pen-to-square`, `image`, `camera`, `key`
