# BCO-DMO submission tool: LLM quick prompts

`quick-prompts.json` holds the **Quick Prompts** shown on the LLM page of a
dataset submission in the submission tool. The submission API reads this file
from the `main` branch of this repository, so editing it here changes the
prompts data managers see, without a code deployment.

## Making a change

1. Edit `quick-prompts.json` (on GitHub directly, or clone, edit, commit, push).
2. Merge/push to `main`.
3. In the submission tool, open any submission, then **DM Actions → Refresh
   Quick Prompts**. The API caches the file and only re-reads it on a new
   deployment or when that button is pressed.

If the file is not valid JSON or fails the checks below, the API keeps serving
the previous prompts and the refresh button shows the error, so a mistake
never leaves the LLM page without prompts. The `Validate JSON` GitHub Action
also checks every push.

## File format

```json
{
  "quickPrompts": [
    {
      "id": "extract_timezone",
      "label": "Extract Timezone",
      "icon": "calendar",
      "includePublications": false,
      "fileSelection": "none",
      "prompt": [
        "First line of the prompt.",
        "",
        "Third line. Each array entry is one line; an empty string is a blank line."
      ]
    }
  ]
}
```

Prompts appear in the order they are listed.

| Field                 | Required | Meaning                                                                                                                                                                                                                                 |
| --------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                  | yes      | Unique, stable identifier: lowercase letters, numbers and underscores. It is recorded with every LLM conversation and in usage reporting, so **keep an existing id when editing its prompt**, and pick a new id for a new prompt.         |
| `label`               | yes      | Text shown on the button.                                                                                                                                                                                                             |
| `prompt`              | yes      | The prompt text. Either one string, or an array of strings that are joined with newlines (easier to read and diff).                                                                                                                       |
| `icon`                | no       | Icon next to the label. One of `book`, `calendar`, `cogs`, `list`, `user`, `file`, `table`, `search`, `globe`, `flask`, `comments`. Anything else, or no value, shows a generic icon.                                                |
| `includePublications` | no       | `true` or `false` ticks or unticks the "Include publications" option when the prompt is chosen. Leave it out to keep whatever the user had set.                                                                                           |
| `fileSelection`       | no       | What happens to the "Files" selection when the prompt is chosen: `none` clears it (default), `parameterFiles` selects every data file that has parameters defined, `keep` leaves it alone.                                                |
