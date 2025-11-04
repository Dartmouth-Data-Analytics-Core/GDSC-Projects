# GDSC: Building a new project SOP
**Author: Mike Martinez, November, 2025**

## Overview

This standard operating procedure (SOP) describes the standard procedure for core personnel when creating and logging a new project repository within the [Dartmouth Data Analytics Core Github Organization](https://github.com/Dartmouth-Data-Analytics-Core). Please follow these steps to ensure:

- Consistent project naming and structure
- Proper tracking in the [GDSC-Projects repo](https://github.com/Dartmouth-Data-Analytics-Core/GDSC-Projects)
- Accurate updates to statistics dashboard

## Initializing a project repo
1. **Create the repository on github**
  - Create a new private github repository initialized with a README.md  
  - Naming convention should be as follows: `YYMMDD-Client-Description`
    - Example: `260101-Smith-kidney-scRNASeq`

2. **Clone the repository**
  - On Github Desktop or command-line git clone the newly created repository to the appropriate client folder on Discovery `GMBSR_bioinfo/labs/<client_lastname>`

## Updating the project master list

The [GDSC-Projects repo](https://github.com/Dartmouth-Data-Analytics-Core/GDSC-Projects) maintains a centralized list of **all active projects**. 

Each project entry is used for:

  - Core personell's ability to quickly locate a project directory of interest.
  - Public visibility of our analytical breadth
  - Automated modality tallying via Github Actions

**Important notes**

  - The [tallying sript](https://github.com/Dartmouth-Data-Analytics-Core/GDSC-Projects/blob/main/scripts/tallyModalities.py) runs **automatically** after each push or modification to the README.md, **do not manually edit modality counts**

  - Valid modality aliases are listed in the tallying script under the `ALIASES` section

  - If you introduce a new modality name, add it a an alias in the script to keep the counts harmonized (i.e, RNA-Seq is the same as RNAseq, but if one is not listed in the aliases, they will be counted as separate categories.)

**Adding a new client**

If the client is not already listed, create a new expandable section using a (< details > block) in alphabetical order. If easier, you can also copy a pre-existing block, paste in the correct location, and modify the tabular information as needed

```
<details>
<summary>ClIENT LAST NAME</summary>
  
| Project | Modality | Repo | Date|
|----------|-----------|------|----|
|REPO NAME| DATA MODALITY| [Github](https://github.com/link/to/repo/)| MM/DD/YYYY |

</details>

```

**Adding new projects to existing clients**

If the client already exists, simply add a new row to their project table.

```
| Project | Modality | Repo | Date|
|----------|-----------|------|----|
|REPO NAME| DATA MODALITY| [Github](https://github.com/link/to/repo/)| MM/DD/YYYY |
|NEW PROJECT| DATA MODALITY| [Github](https://github.com/link/to/new_repo/)| MM/DD/YYYY |
```

**Formatting Guidelines**

- `Repo name` should match exactly the Github repository name

- `Modality` should use consistent modality terminology that matches existing aliases, or add a new alias to the tallying script.

- `Repo` should be a hyperlink to the repository called "Github". Use markdown hyperlinks using this formula: ```[Github](link)```

- Date column should be in MM/DD/YYYY format


