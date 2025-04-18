import re
import pyperclip
from jupyter_core.version import pattern

mistral_output = [
[' NOTHING\n\n'],
[' "Marijuana legalization in Colorado"\n\n'],
[' "Although many new laws are controversial, they made it through legislatures..." (This sentence suggests that controversial laws have been passed, which includes the legalization of marijuana in some cases.)\n\n'],
[' NOTHING (The sentence in the article does not support the argument about marijuana legalization.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence does not support the argument that marijuana has been legalized.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence about guns, family leave, and shark fins does not relate to the argument about marijuana being legalized.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence does not support the given argument about marijuana being legalized.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING (There was no mention of marijuana legalization in the article about Illinois and drones.)\n\n'],
[' NOTHING (The article does not discuss or imply anything about the legalization of marijuana.)\n\n'],
[' NOTHING\n\n'],
[" NOTHING (The given article doesn't discuss the legality of marijuana.)\n\n"],
[' NOTHING (The article discusses transgender rights, not the legalization of marijuana.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The given sentence discusses minimum wage and employment for former felons, neither of which is directly related to marijuana being legalized.)\n\n'],
[' NOTHING (The given sentence does not support the argument about marijuana legalization as it pertains to minimum wage increases.)\n\n'],
[' NOTHING (The sentence does not provide information about marijuana being legalized.)\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence does not support the argument that marijuana has been legalized in Rhode Island.)\n\n'],
[' "Colorado became the first U.S. state to fully legalize recreational marijuana use in 2014." (From the article)\n\n   "NOTHING" (If there was no statement about marijuana being legalized in the article)\n\n'],
[' NOTHING (The article discusses privacy rights regarding social media account access, not the legality of marijuana.)\n\n'],
[' Colorado: Marijuana becomes legal in the state for buyers over 21 at a licensed retail dispensary.\n\n'],
[' The following sentence(s) in your article support your argument: "Marijuana has been legalized for recreational use in a number of states."\n\n']
    ]

# ANSI escape codes
BLUE = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'

sample_text = f"""WASHINGTON (CNN) — Not everyone subscribes to a New Year’s resolution, but Americans will be required to follow new laws in 2014.
Some 40,000 measures taking effect range from sweeping, national mandates under Obamacare to marijuana legalization in Colorado, drone prohibition in Illinois and transgender protections in California.
Although many new laws are controversial, they made it through legislatures, public referendum or city councils and represent the shifting composition of American beliefs.
Federal: Health care, of course, and vending machines
The biggest and most politically charged change comes at the federal level with the imposition of a new fee for those adults without health insurance.
For 2014, the penalty is either $95 per adult or 1% of family income, whichever results in a larger fine.
The Obamacare, of Affordable Care Act, mandate also requires that insurers cover immunizations and some preventive care.
Additionally, millions of poor Americans will receive Medicaid benefits starting January 1.
Thousands of companies will have to provide calorie counts for products sold in vending machines.
Local: Guns, family leave and shark fins
Connecticut: While no national legislation was approved to tighten gun laws a year after the Newtown school shooting, Connecticut is implementing a final round of changes to its books: All assault weapons and large capacity magazines must be registered.
Oregon: Family leave in Oregon has been expanded to allow eligible employees two weeks of paid leave to handle the death of a family member.
California: Homeless youth are eligible to receive food stamps. The previous law had a minimum wage requirement.
Delaware: Delaware is the latest in a growing number of states where residents can no longer possess, sell or distribute shark fins, which is considered a delicacy in some East Asian cuisine.
Illinois and drones
Illinois: passed two laws limiting the use of drones. One prohibits them from interfering with hunters and fisherman. The measure passed after the group People for the Ethical Treatment of Animals said it would use drones to monitor hunters. PETA said it aims through its “air angels” effort to protect against “cruel” and “illegal” hunting.
Also in Illinois, another law prohibits the use of drones for law enforcement without a warrant.
Gender and voting identity
California: Students can use bathrooms and join school athletic teams “consistent with their gender identity,” even if it’s different than their gender at birth.
Arkansas: The state becomes the latest state requiring voters show a picture ID at the voting booth.
Minimum wage and former felon employment
Workers in 13 states and four cities will see increases to the minimum wage.
While most amount to less than 15 cents per hour, workers in places like New Jersey, and Connecticut.
New Jersey residents voted to raise the state’s minimum wage by $1 to $8.25 per hour. And in Connecticut, lawmakers voted to raise it between 25 and 75 cents to $8.70. The wage would go up to $8 in Rhode Island and New York.
California is also raising its minimum wage to $9 per hour, but workers must wait until July to see the addition.
Rhode Island: It is the latest state to prohibit employers from requiring job applicants to signify if they have a criminal record on a job application.
Social media and pot
Oregon: Employers and schools can’t require a job or student applicant to provide passwords to social media accounts.
Colorado: Marijuana becomes legal in the state for buyers over 21 at a licensed retail dispensary.
(Sourcing: much of this list was obtained from the National Conference of State Legislatures)."""

formatted_evidence=""

# ========================
# BUILDING THE RTF OUTPUT
# ========================
formatted_rtf = r"""{\rtf1\ansi\deff0{\colortbl ;\red0\green112\blue192;}"""  # light blue

for i, (highlighted_text, article_sentence) in enumerate(zip(mistral_output, sample_text.split("\n"))): #iterate through each sentence in sample text
    # Remove formatting from article_sentence
    highlighted_text = highlighted_text[0].replace("\"", "");

    if highlighted_text.startswith("NOTHING") or not highlighted_text:
        formatted_rtf += article_sentence + r"\line "
        continue

    print(i, article_sentence)
    print(highlighted_text.split()[0])
    if "NOTHING" not in highlighted_text.split()[0]:   # check if we can skip if phrase starts with "NOTHING"
        # Go sequentially through each word in mistral output. If that word is in sample_text, highlight it. This is how we weed out the faulty outputs that write summaries and only get the verbatim phrases
        print("*"*80)
        for mistral_word in highlighted_text.split():
            print(mistral_word + " | " + article_sentence)
            b = False
            for word in article_sentence.split():
                if word.lower() == mistral_word.lower() and not b:
                    print("replacing->", word.lower(), mistral_word.lower())
                    # article_sentence = article_sentence.replace(mistral_word, f"{BOLD}{BLUE}{mistral_word}{END}")
                    # article_sentence = article_sentence.replace(mistral_word, f"B{mistral_word}E")
                    pattern = rf"\b{re.escape(mistral_word)}"
                    replacement = r"{\b\ul\cf1 " + mistral_word + r"}"

                    article_sentence = re.sub(pattern, f"{BLUE}{BOLD}{mistral_word}{END}", article_sentence,
                                              flags=re.IGNORECASE)
                    b = True

    formatted_evidence+=article_sentence + "\n"

print("=="*50 + "\n\n" + formatted_evidence)