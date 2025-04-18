import win32clipboard as wc
import win32con
from searchAndHighlight import highlight_extracted_words

def copy_rtf_to_clipboard(rtf_text):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_TEXT, rtf_text.encode('windows-1252'))  # Optional plain-text fallback
    wc.SetClipboardData(wc.RegisterClipboardFormat("Rich Text Format"), rtf_text.encode('windows-1252'))
    wc.CloseClipboard()


mistral_output = [
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence in the article does not directly support or contradict your argument about Trump\'s tariffs being "bad.")\n\n'],
[' NOTHING\n\n'],
[' "The 10% tariff on goods from most nations means a $10 product would have a $1 tax on top - taking the total cost to $11 (£8.35). The 145% charge on some Chinese goods would take the cost of a $10 product to $24.50 (£18.60)"\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[" NOTHING (The sentence does not support the argument that Trump's tariffs are bad.)\n\n"],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' NOTHING\n\n'],
[' "A 10% tariff on goods from China to the US was unveiled in February - alongside the taxes on products from Mexico and Canada. Tariffs for China have since increased to 125%. However, for some Chinese products taxes will be set at 145%, due to a previous 20% levy for those producing the drug fentanyl."\n\n'],
[' NOTHING\n\n'],
[' NOTHING (The sentence does not support the provided argument that "trump\'s tariffs are bad")\n\n'],
[" NOTHING (The sentence does not provide any information about Trump's tariffs being good or bad.)\n\n"],
[" NOTHING (The sentence does not support the argument that Trump's tariffs are bad.)\n\n"],
[' Many economists expect tariffs to push up prices across a range of imported goods... Some firms may also decide to import fewer foreign goods, which could make those that are available more expensive... The price of goods manufactured in the US using imported components may also rise. For example, car parts typically cross the US, Mexican and Canadian borders multiple times before a vehicle is completely assembled.\n\n'],
[' "Car prices had already been expected to increase as a result of earlier tariffs, which remain in place."\n\n'],
[" NOTHING (The article provides no information about Trump's tariffs being good or bad.)\n\n"],
[' "Many people are affected by stock market price falls, even if they don\'t invest in shares directly, because of the knock-on effect on pensions, jobs and interest rates."\n\n'],
[' NOTHING (The given article does not provide any direct information supporting that Trump\'s tariffs are "bad.")\n\n'],
[' NOTHING (The sentence does not directly support your argument.)\n\n'],
[" NOTHING (The article does not address the argument about Trump's tariffs being good or bad.)\n\n"],
[' "Prime Minister Sir Keir Starmer said \'clearly there will be an economic impact\' from the 10% tariff."\n\n'],
[' Jaguar Land Rover said it would "pause" all shipments to the US as it worked to "address the new trading terms".\n\n'],
[" NOTHING (The article doesn't state that Trump's tariffs are good, but it doesn't directly refute the claim either.)\n\n"],
[" NOTHING (The article does not provide information about whether or not Trump's tariffs are good or bad.)\n\n"],
[' NOTHING\n\n'],
    ]

sample_text = f"""What are tariffs and why is Trump using them?
4 days ago Share Save Jennifer Clarke BBC News Share Save
Watch: What is a tariff? The BBC's Adam Fleming explains
In a growing trade war, US President Donald Trump has placed tariffs of up to 145% on Chinese goods. China has hit back with 125% on US products. Trump has also introduced a 10% tax on goods from the vast majority of other countries, while pausing much higher rates for dozens of nations for 90 days. He argues that tariffs will boost US manufacturing and protect jobs, but the world economy has been thrown into chaos and prices are expected to rise.
What are tariffs and how do they work?
Tariffs are taxes charged on goods bought from other countries. Typically, they are a percentage of a product's value. The 10% tariff on goods from most nations means a $10 product would have a $1 tax on top - taking the total cost to $11 (£8.35). The 145% charge on some Chinese goods would take the cost of a $10 product to $24.50 (£18.60). Companies that bring foreign goods into the US have to pay the tax to the government. They may pass some or all of the increased cost on to customers. Follow live: Trump suggests tariff exemption for China-made smartphones could be short-lived
Trump steps back from cliff edge of global trade war
Why is Trump using tariffs?
Trump says tariffs will encourage US consumers to buy more American-made goods, increase the amount of tax raised and lead to huge levels of investment in the country. He wants to reduce the gap between the value of goods the US buys from other countries and those it sells to them. He argues that America has been taken advantage of by "cheaters" and "pillaged" by foreigners. The US president has made other demands alongside tariffs. The first announced during his current term targeted China, Mexico and Canada, after he said he wanted them to do more to stop migrants and illegal drugs reaching the US. Trump has strongly defended his tariffs policy but influential voices within his Republican Party have joined opposition Democrats and foreign leaders in attacking the measures. Why Beijing is not backing down on tariffs
Is the US making $2bn a day from tariffs?
Reuters China now produces 60% of the world's electric cars – a large proportion of them made by its own homegrown brands
What has Trump announced on tariffs?
Since Trump's inauguration in January there has been a flurry of announcements on tariffs, with other countries scrambling to respond. Mexico and Canada: Canada and Mexico were targeted by Trump back in February during an earlier round of raised tariffs. The president announced a 25% tax on exports from both countries to the US and a 10% levy on Canadian energy. There have since been a number of exemptions and delays. Trump's "baseline" 10% rate does not apply to them. Steel and aluminium: A 25% import tax on all steel and aluminium entering the US, including products made from these metals took effect on 12 March. Cars: The White House announced in March that 25% duties on cars would apply from 2 April. A similar 25% levy on car parts is due to come in by 3 May. Higher tariffs paused: Tariffs on roughly 60 countries, which were described by the US president as the "worst offenders", were introduced on 9 April. Trump then announced a 90-day pause, during which the 10% "baseline" rate will be paid, excluding China. China: A 10% tariff on goods from China to the US was unveiled in February - alongside the taxes on products from Mexico and Canada. Tariffs for China have since increased to 125%. However, for some Chinese products taxes will be set at 145%, due to a previous 20% levy for those producing the drug fentanyl. China put tariffs on US imports at 125% from 12 April and has said it will not respond to any further US increases because they will become a "joke". Smartphones and computers: An exemption for some electronic devices including smartphones and computers, backdated to 5 April, was announced on 12 April. But Trump then said exemptions for technology from China could be short lived. BBC Verify: How were Donald Trump's tariffs calculated?
How much trade is there between the US and China?
The US currently runs a trade deficit with China. In 2024, the US imported far more from China ($440bn) than Beijing imported from America ($145bn). In his first term as president, Trump imposed significant tariffs on China, which were retained and expanded by his successor Joe Biden. Together those trade barriers helped to reduce the amount the US bought from China from 21% of America's total imports in 2016 to 13% in 2024. However, China still ships everything from iPhones to children's toys to the US. Analysts have pointed out that some Chinese goods enter the US via neighbouring South East Asian countries, which could mean they can avoid the tariffs of up to 145% Why Trump is hitting China on trade - and what might happen next
What would a US-China trade war do to the world economy?
Will prices go up for US consumers?
Many economists expect tariffs to push up prices across a range of imported goods, as firms pass on some or all of their increased costs. The products affected could include everything from clothing to coffee and alcohol to electronics. Some firms may also decide to import fewer foreign goods, which could make those that are available more expensive. The price of goods manufactured in the US using imported components may also rise. For example, car parts typically cross the US, Mexican and Canadian borders multiple times before a vehicle is completely assembled.
Car prices had already been expected to increase as a result of earlier tariffs, which remain in place. The cost of a car made using parts from Mexico and Canada alone could rise by $4,000-$10,000 (£3,035 - £7,588) depending on the vehicle, according to analysts at the Anderson Economic Group.
What has happened to stock markets?
Trump's tariffs announcements have caused significant volatility on global stock markets. Stock markets are where firms sell shares in their business. They reflect the best guess of what every company in the world is worth and what their future profits will be. Many people are affected by stock market price falls, even if they don't invest in shares directly, because of the knock-on effect on pensions, jobs and interest rates. How does it affect me if share prices fall?
Stocks, tariffs and pensions - your questions answered
How will Trump's tariffs affect the UK?
PA Media
The UK exported around £58bn of goods to the US in 2024, mainly cars, machinery and pharmaceuticals. It was already due to be affected by the earlier tariffs targeting steel, aluminium and car imports. Prime Minister Sir Keir Starmer said "clearly there will be an economic impact" from the 10% tariff. The UK is looking to negotiate a trade deal to soften the 10% tariffs, but one of President Trump's advisers suggests any such deal would have to be "extraordinary". The UK government has so far not announced any taxes on US imports. However, it is drawing up a list of US products it could hit with retaliatory tariffs.
Following the announcement of tariffs, carmaker Jaguar Land Rover said it would "pause" all shipments to the US as it worked to "address the new trading terms". Economists have warned US tariffs could knock the UK's economy off course and make it harder for the government to hit its borrowing rules. How the prime minister might tackle impact of Trump tariffs
How exposed is the UK to Trump's tariff chaos?
How have other countries responded to Trump's decision to pause the tariffs?
For countries on Donald Trump's so-called "worst offenders" list, there was a sigh of relief when tariffs were temporarily downgraded to 10%. But the impact of the lower rate remains a serious concern for them. The European Union is among those seeking a trade deal with the US during this 90-day higher tariff pause. The bloc is also "developing retaliatory measures" in case talks fail, EU chief Ursula von der Leyen has said. Poland's Prime Minister Donald Tusk urged all parties to "make the best" of the 90 day pause, stressing that maintaining strong relations with the US "is a common responsibility of Europeans and Americans". Germany's incoming Chancellor Friedrich Merz said the pause proves a united European approach to trade has a positive effect, adding: "Europeans are determined to defend ourselves". Vietnam's Deputy Prime Minister Ho Duc Phoc said the US and Vietnam expect to start "negotiations on a bilateral trade agreement", which "would include tariff agreements". Canada, which has been targeted by tariffs above 10%, introduced a 25% tariff on some vehicles from the US on 9 April. See the Trump tariffs list by country"""

# ========================
# BUILDING THE RTF OUTPUT
# ========================
# Use this for RTF highlight
begin = r"{\highlight1\b\ul "
end = r"}"

# RTF header and footer
rtf_header = r"""{\rtf1\ansi\deff0{\colortbl ;\red204\green255\blue255;}"""  # Light blue highlight
rtf_footer = "}"

# Process
formatted_rtf_body = ""

for i, (extracted_text, article_sentence) in enumerate(zip(mistral_output, sample_text.split("\n"))): #iterate through each sentence in sample text
    # Remove formatting from article_sentence
    extracted_text = extracted_text[0].replace("\"", "");
    highlighted_phrase = article_sentence
    print(i, article_sentence)
    print(extracted_text.split()[0])
    if "NOTHING" not in extracted_text.split()[0]:   # check if we can skip if phrase starts with "NOTHING"
        # get the output and add to formatted_evidence
        highlighted_phrase = highlight_extracted_words(article_sentence, extracted_text, beginning_marker=begin, ending_marker=end)

    formatted_rtf_body += highlighted_phrase + r"\line "

rtf_body = formatted_rtf_body + r"\line "
full_rtf = rtf_header + formatted_rtf_body + rtf_footer
copy_rtf_to_clipboard(full_rtf)

print("=="*50 + "\n\n" + formatted_rtf_body)
print(full_rtf)