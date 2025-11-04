# GDSC: Building a new project SOP

## Initializing a project repo

1. Create a new private github repository initialized with a README.md  
2. Naming convention should be as follows: `YYMMDD-Client-Description`
3. On Github Desktop or Git, clone the repository to the respective client folder on Discovery within GMBSR_bioinfo. For example, if the project is 260101-Smith-RNASeq, clone the repo to GMBSR_bioinfo/Labs/smith

## Updating the project master list

For organization and a public-facing record of our work it is important to update the master list of project housed in the [GDSC-Projects Repo](tps://github.com/Dartmouth-Data-Analytics-Core/GDSC-Projects/). The README.md
on that repository contains drop down lists of projects, split by client. Client names follow alphabetical order. Information included in each client table includes the repo name, a data-modality category, a link to the
private repo (which only GDSC team members can access) and the date the repo was added. A Github action is set such that every time this README.md is modified, or a change is pushed to this repo, a tally of modalities 
will be updated. **You do not need to manually change this in the readme!** The script which completes the tallying is set to accept harmonized alises for each data modality, but new terms can be addedd in as well within the 
script [here](https://github.com/Dartmouth-Data-Analytics-Core/GDSC-Projects/blob/main/scripts/tallyModalities.py) under the `ALIASES` section. Any term not included in the alises will be counted as its own category.

**For new clients not already listed:**

1. Create a new header for this client by alphabetically placing their name within the list using this structure: *You can just copy and paste a block from the README.md and edit as necessary!*

```
<details>
<summary>ClIENT LAST NAME</summary>
  
| Project | Modality | Repo | Date|
|----------|-----------|------|----|
|REPO NAME| DATA MODALITY| [Github](https://github.com/link/to/repo/)| MM/DD/YYYY |

</details>

```

**Formatting details**

- Repo name should be exactly as it appears on github
- Modality should typically match one of the aliases in `scripts/tallyModalities.py`, or a new aslias should be added directly to the script (ex, try and avoid having RNA-Seq in some places and RNAseq in others)
- Repo should be a clickable hyperlink called "Github". To create hyperlinks in markdown use this convention: [Github](htpps://github.com/link/to/repo/)
- Date column should be in MM/DD/YYYY format


**For clients already listed**

1. Locate the client on the README.md and edit to add a new row to their table

```
| Project | Modality | Repo | Date|
|----------|-----------|------|----|
|REPO NAME| DATA MODALITY| [Github](https://github.com/link/to/repo/)| MM/DD/YYYY |
|NEW PROJECT| DATA MODALITY| [Github](https://github.com/link/to/new_repo/)| MM/DD/YYYY |

```


