"""
Little Lights — Daily WhatsApp Story Sender (Twilio)
=====================================================
Sends one story per day to WhatsApp using the Twilio WhatsApp API.
Splits each story into two messages to stay under the 1600-char limit.

SETUP:
1. Make sure your Twilio WhatsApp sandbox is active at:
   https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
2. The recipient (+919886303637) must join the sandbox by sending
   the join code to +14155238886 on WhatsApp (one-time step).
3. Install dependency:  pip install requests
4. Test once:  python3 send_story.py
"""

import json
import requests
from datetime import date
from pathlib import Path
import os

# ── CONFIG ──────────────────────────────────────────────────────────
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "AC9ec0af02600f5bfdf16037f455a8afd5")
TWILIO_AUTH_TOKEN  = os.environ.get("TWILIO_AUTH_TOKEN",  "dae232912aeec2795e13ec719b9bd3d7")
FROM_NUMBER        = os.environ.get("TWILIO_FROM",        "whatsapp:+14155238886")
TO_NUMBER          = os.environ.get("TWILIO_TO",          "whatsapp:+919886303637")

# Auto-fix missing whatsapp: prefix
if not FROM_NUMBER.startswith("whatsapp:"): FROM_NUMBER = "whatsapp:" + FROM_NUMBER
if not TO_NUMBER.startswith("whatsapp:"):   TO_NUMBER   = "whatsapp:" + TO_NUMBER
# ────────────────────────────────────────────────────────────────────

TRACKER_FILE = Path(__file__).parent / "story_tracker.json"

# All 15 stories — WhatsApp-formatted text
STORIES = [
    {
        "id": 1,
        "title": "Ganesha and the Greedy Moon",
        "age": "Ages 2–4 🧸",
        "tradition": "Hindu 🕉️",
        "text": (
            "🌙 One full-moon night, little Ganesha — the elephant-headed god — went to a big feast. 🎉\n\n"
            "There were mountains of round, golden laddoos! 🟡🟡\n\n"
            "Ganesha loved laddoos SO much. He ate one… then two… then TEN! 😋\n\n"
            "His big tummy became SO round that when he tried to ride his tiny mouse friend home — PLOP! — he fell right off! 🐭💨\n\n"
            "The Moon saw this and started to laugh. \"Ha ha ha! Look at the fat elephant!\" 😂🌕\n\n"
            "Ganesha felt sad. 😢 He looked up at the Moon and said, \"Moon, it is not kind to laugh at someone who falls. "
            "You will become dark so no one laughs at YOU!\"\n\n"
            "And that is why the Moon goes from big to small every month — to remember never to be unkind. 🌕🌔🌓🌒🌑"
        ),
        "think": "🤔 *Think About It!*\nHave you ever laughed at someone when they fell? How do you think they felt? What could you do instead?",
        "moral": "✨ *Today's Lesson:* Kindness matters more than being clever. Never laugh at someone else's struggles."
    },
    {
        "id": 2,
        "title": "Baby Krishna's Butter Secret",
        "age": "Ages 2–4 🧸",
        "tradition": "Hindu 🕉️",
        "text": (
            "🌅 In a village called Vrindavan, little Krishna had the BIGGEST secret. 🤫\n\n"
            "Every morning, Mama Yashoda would wake up and find her butter pots empty! 🫙➡️😮\n\n"
            "But little Krishna had blue skin, curly hair, and the most mischievous smile. 😏\n\n"
            "He would sneak into the kitchen — tip-toe, tip-toe! 🦶🦶 — climb up the shelves, and eat all the butter! 😋\n\n"
            "One day, Mama Yashoda caught him! His face was covered in white butter. Even the monkeys had butter on their noses! 🐒🐒\n\n"
            "\"Krishna! Did you eat my butter?\" she asked.\n\n"
            "Krishna looked at Mama, put his little hand over his mouth… and started LAUGHING. 😂\n\n"
            "Mama Yashoda couldn't help but laugh too. ❤️\n\n"
            "She hugged him and said, \"You mischievous boy! Share the butter — don't take it all yourself!\"\n\n"
            "And Krishna promised. He brought butter for ALL the children in the village that day. 🧈👶👧🧒"
        ),
        "think": "🤔 *Think About It!*\nKrishna loved butter so much he forgot to share. Is there something YOU love to eat? Can you share it with someone today?",
        "moral": "✨ *Today's Lesson:* Sharing what we love makes everyone — including us — happier."
    },
    {
        "id": 3,
        "title": "Guru Nanak's Magic Langar",
        "age": "Ages 2–4 🧸",
        "tradition": "Sikh 🪯",
        "text": (
            "🌄 Long ago, a young boy named Nanak walked with his father through a village.\n\n"
            "His papa gave him some money and said, \"Go make a good deal, my son!\" 💰\n\n"
            "On the way, Nanak saw a group of very hungry men sitting under a tree. Their tummies were growling. 😔\n\n"
            "Nanak's heart felt warm and sad at the same time. ❤️\n\n"
            "\"I know the BEST deal I can make!\" he thought. ✨\n\n"
            "He ran to the market and bought baskets full of food — rice, dal, roti, vegetables! 🍚🫓🥦\n\n"
            "He set up a big spread under the tree and called everyone to eat. \"Come! Everyone is welcome! Sat Sri Akal!\" 🙏\n\n"
            "People came — rich and poor, young and old — and everyone ate together. 🧑‍🤝‍🧑\n\n"
            "When his papa heard, he was first surprised… then he smiled. 🥹\n\n"
            "\"You are right, Nanak. The best deal is taking care of people.\"\n\n"
            "And that is how the tradition of Langar — the free kitchen where everyone eats together — began! 🍲🍲🍲"
        ),
        "think": "🤔 *Think About It!*\nNanak chose to feed hungry people instead of buying things. Can you think of one way you can help someone today?",
        "moral": "✨ *Today's Lesson:* Sharing food and kindness is the greatest gift of all."
    },
    {
        "id": 4,
        "title": "Little Mahavir and the Crying Ant",
        "age": "Ages 2–4 🧸",
        "tradition": "Jain ☮️",
        "text": (
            "🌿 One sunny morning, little Mahavir was walking in the garden with his friends.\n\n"
            "They were laughing and running when suddenly, Mahavir stopped. 🛑\n\n"
            "\"What's wrong?\" his friends asked.\n\n"
            "Mahavir pointed to a tiny puddle near their feet. Inside it, a little ant was splashing and struggling! 🐜💦\n\n"
            "\"It's just an ant,\" said one friend. \"Come, let's play!\"\n\n"
            "But Mahavir knelt down. Gently — SO gently — he picked up a leaf. 🍃\n\n"
            "He held the leaf near the ant. The ant climbed on.\n\n"
            "Mahavir placed the leaf carefully on dry ground. The ant wiggled its antennae. It was safe! ✨\n\n"
            "\"Thank you,\" the ant seemed to say as it walked away. 🐜\n\n"
            "Mahavir's heart felt SO warm inside. 🌞\n\n"
            "His friends watched quietly. Then one by one, they came back.\n\n"
            "\"We want to help too,\" they said.\n\n"
            "From that day on, they all walked more slowly and carefully — watching where their feet went. 🦶💕"
        ),
        "think": "🤔 *Think About It!*\nMahavir helped a tiny ant nobody else noticed. Can you look for one small living thing today and be gentle with it?",
        "moral": "✨ *Today's Lesson:* Every creature — big or small — deserves kindness and care."
    },
    {
        "id": 5,
        "title": "Ibrahim Counts the Stars",
        "age": "Ages 2–4 🧸",
        "tradition": "Islamic ☪️",
        "text": (
            "🌙 Every night, little Ibrahim would lie on the soft grass and look up at the sky.\n\n"
            "One two three… he tried to count the stars. ⭐🌟✨\n\n"
            "\"One, two, three, four… so many! I can't count them all!\" he giggled.\n\n"
            "Ibrahim wondered: who painted the sky with so many sparkly lights?\n\n"
            "He asked his mama. \"Mama, who made all the stars?\"\n\n"
            "Mama smiled and sat beside him. \"Allah made them, my dear — and He made the moon, the sun, the trees, the birds, and YOU!\" 🌙☀️🌳🐦\n\n"
            "\"He made ME?\" Ibrahim's eyes went wide. 👀\n\n"
            "\"Yes! And He loves you more than all the stars put together.\" ❤️\n\n"
            "Ibrahim looked back up at the sky. There were SO many stars. He tried to imagine love even bigger than that.\n\n"
            "He couldn't — but he smiled anyway. 😊\n\n"
            "\"I love Allah too,\" he said quietly.\n\n"
            "And then he made a little dua — a tiny prayer — before he fell asleep. 🤲💫"
        ),
        "think": "🤔 *Think About It!*\nIbrahim found wonder in the night sky! What is one beautiful thing around you right now that makes you feel amazed?",
        "moral": "✨ *Today's Lesson:* Wonder and gratitude open our hearts to the beauty all around us."
    },
    {
        "id": 6,
        "title": "Hanuman's Giant Leap",
        "age": "Ages 5–7 🚀",
        "tradition": "Ramayana 🏹",
        "text": (
            "🌊 The ocean stretched forever. Nobody thought anyone could cross it.\n\n"
            "Lord Rama's beloved Sita had been taken to Lanka — an island across a vast sea — by the demon king Ravana. 😤\n\n"
            "Rama's heart ached. \"How will we reach her?\" he worried.\n\n"
            "His loyal friend Hanuman stepped forward. His eyes burned with devotion. \"I will go, my Lord.\"\n\n"
            "The other animals gasped. \"The ocean is impossible to cross!\"\n\n"
            "But Hanuman closed his eyes, thought of Rama, and felt a power rise inside him like a roaring fire. 🔥\n\n"
            "He climbed to the top of a mountain. He took a deep breath.\n\n"
            "He LEAPED! 💨\n\n"
            "His body flew through the clouds, he grew bigger and bigger, and with a mighty WHOOSH, he soared across the entire ocean! 🌊🌊🌊\n\n"
            "He landed in Lanka with a THUD! 🏝️\n\n"
            "He found Sita, gave her Rama's ring as a sign, and whispered: \"Be strong, Mata. Rama is coming for you.\" 💍\n\n"
            "Sita's eyes filled with tears — but they were happy tears. 😭❤️\n\n"
            "When Hanuman returned, everyone cheered. Rama held Hanuman's hands and said:\n\n"
            "\"You did the impossible today — not because you are strong, but because you believed.\"\n\n"
            "🐒 Hanuman smiled. \"When you believe, my Lord, anything is possible.\""
        ),
        "think": "🤔 *Think About It!*\nHanuman thought he couldn't do it — then he believed in himself and did something amazing. Is there something you think you can't do? What might happen if you believed you COULD?",
        "moral": "✨ *Today's Lesson:* Faith in yourself — and love for those you care about — can make you do extraordinary things."
    },
    {
        "id": 7,
        "title": "Eklavya's Silent Teacher",
        "age": "Ages 5–7 🚀",
        "tradition": "Mahabharata ⚔️",
        "text": (
            "🌲 Deep in the forest, a young boy named Eklavya dreamed of becoming the world's greatest archer.\n\n"
            "He went to the royal teacher Dronacharya and bowed low. \"Please teach me archery, Guruji.\"\n\n"
            "Drona looked at Eklavya — he was from a forest tribe, not a prince. Drona shook his head. \"I only teach royals.\"\n\n"
            "Eklavya walked away. His heart hurt. But he did not cry for long. 💪\n\n"
            "He went deep into the forest, gathered clay, and made a statue of Dronacharya. 🗿\n\n"
            "Every single day, he bowed to the statue and said, \"You are my teacher.\" Then he practiced archery — alone — for HOURS. 🏹🏹🏹\n\n"
            "Days passed. Weeks. Months.\n\n"
            "One day, Drona and his students found a dog with an arrow in its open mouth — but the dog was not hurt! Just silenced.\n\n"
            "\"Who did this?!\" Drona was amazed. No one had that kind of skill.\n\n"
            "They found Eklavya, covered in dust, still practicing.\n\n"
            "\"You… you taught yourself?\" Drona whispered, stunned.\n\n"
            "\"You were my teacher,\" Eklavya said, pointing to the statue. \"In my heart, you always were.\"\n\n"
            "Drona's eyes filled with tears. He had underestimated this boy.\n\n"
            "And Eklavya had proven: no door — not even a closed one — can stop a determined heart. 🌟"
        ),
        "think": "🤔 *Think About It!*\nEklavya couldn't find a teacher, so he created one in his imagination. Have you ever practiced something even when no one helped you? What happened?",
        "moral": "✨ *Today's Lesson:* Determination and belief in yourself can teach you more than any classroom."
    },
    {
        "id": 8,
        "title": "Mahavir and the Angry Snake",
        "age": "Ages 5–7 🚀",
        "tradition": "Jain ☮️",
        "text": (
            "🌿 Young Mahavir walked barefoot through the forest, meditating and at peace.\n\n"
            "Suddenly — HISSSS! 🐍\n\n"
            "A large cobra rose up from the path, hood spread wide, eyes gleaming. It was angry and afraid.\n\n"
            "The people behind Mahavir screamed and ran. \"Run! It will bite you!\"\n\n"
            "But Mahavir stopped. He stood completely still. 🧘\n\n"
            "He looked at the snake — not with fear, but with deep, gentle eyes. As if to say: \"I will not hurt you. I promise.\"\n\n"
            "The cobra swayed. It hissed again. Still Mahavir did not move.\n\n"
            "Slowly… slowly… the snake lowered its hood. 🐍⬇️\n\n"
            "It slithered off the path and disappeared into the grass.\n\n"
            "Everyone came back, mouths open. \"How did you do that?!\"\n\n"
            "Mahavir smiled. \"The snake was not evil. It was scared. All living things want to be safe. When I showed it I meant no harm, it felt no need to harm me.\"\n\n"
            "One child asked, \"But what if it had bitten you?\"\n\n"
            "Mahavir said, \"Even then, I would not have blamed it. Anger answered with anger only makes more anger. Peace answered with peace — that is the way.\" ☮️"
        ),
        "think": "🤔 *Think About It!*\nWhen someone is mean to you, do you want to be mean back? What do you think might happen if you stayed calm instead, like Mahavir did?",
        "moral": "✨ *Today's Lesson:* Non-violence (ahimsa) is not just about not hurting — it is about responding to fear with peace."
    },
    {
        "id": 9,
        "title": "The Five Brave Ones",
        "age": "Ages 5–7 🚀",
        "tradition": "Sikh 🪯",
        "text": (
            "🌅 It was the festival of Baisakhi, and thousands of Sikhs had gathered at Anandpur Sahib.\n\n"
            "Guru Gobind Singh stood before the crowd. His voice rang out like thunder:\n\n"
            "\"Is there anyone here willing to give their head for Waheguru — for truth and justice?\"\n\n"
            "The crowd went silent. People looked at each other nervously. 😰\n\n"
            "Then — one hand went up. A man named Daya Ram stepped forward. \"I am ready, Guru Ji.\" 🙋\n\n"
            "Guru Ji took him inside the tent. A moment later — THWACK! 😮\n\n"
            "Everyone gasped. Then the Guru came out again. \"I need another brave one.\"\n\n"
            "This happened five times. Five brave souls.\n\n"
            "But then — Guru Ji came out of the tent… with ALL FIVE MEN! Alive! Dressed in blue, with turbans, faces glowing. ✨\n\n"
            "\"I was testing your courage,\" Guru Ji said. \"These five — the Panj Pyare, my Beloved Five — are the first members of the Khalsa. People who stand for truth even when it is hard.\"\n\n"
            "The crowd erupted in cheers. \"Waheguru! Waheguru!\" 🎉\n\n"
            "The five men smiled — not because they were heroes. But because they had overcome their own fear.\n\n"
            "And THAT was the real victory. 💪"
        ),
        "think": "🤔 *Think About It!*\nEach of the five men was scared but still stepped forward. Have you ever done something even though you were scared? How did it feel after?",
        "moral": "✨ *Today's Lesson:* True bravery is not the absence of fear — it is doing what is right even when you are afraid."
    },
    {
        "id": 10,
        "title": "Yusuf and the Colorful Coat",
        "age": "Ages 5–7 🚀",
        "tradition": "Islamic ☪️",
        "text": (
            "🌈 Prophet Yusuf had a coat of many colors — a gift from his beloved father. It shimmered like a rainbow. 🧥✨\n\n"
            "His brothers were jealous. \"Why does Papa love Yusuf more?\" they grumbled.\n\n"
            "One day, filled with jealousy, they threw Yusuf into a deep well and sold him to passing traders. 😢\n\n"
            "Yusuf was taken far away to Egypt. He had nothing. Not even his coat.\n\n"
            "But Yusuf didn't give up. He kept his heart clean of anger and bitterness. 💚\n\n"
            "He worked hard. He was honest. He was kind.\n\n"
            "In Egypt, he became known for his wisdom — he could understand dreams! 💭✨\n\n"
            "Years passed. A great famine struck the land. People came from everywhere for food — including his brothers.\n\n"
            "They didn't recognize the powerful man in front of them.\n\n"
            "\"I am Yusuf,\" he said gently. \"Your brother.\"\n\n"
            "They trembled, expecting punishment. 😨\n\n"
            "But Yusuf opened his arms. \"Do not be afraid. What you meant for harm, Allah used for good. I forgive you.\" 🤗\n\n"
            "His brothers wept. His father was brought and reunited with him. 🥹\n\n"
            "Yusuf's patience had made something beautiful from something broken. 🌸🌧️🌸"
        ),
        "think": "🤔 *Think About It!*\nYusuf was treated unfairly but chose forgiveness over revenge. Has someone ever hurt you? How hard would it be to forgive them?",
        "moral": "✨ *Today's Lesson:* Patience and forgiveness are the greatest strengths. What seems like a setback can lead to something wonderful."
    },
    {
        "id": 11,
        "title": "Arjuna's Big Question",
        "age": "Ages 8–10 📚",
        "tradition": "Mahabharata ⚔️",
        "text": (
            "⚔️ The two armies stood facing each other on the field of Kurukshetra.\n\n"
            "Arjuna, the greatest archer in the world, stood in the chariot driven by his dear friend Krishna.\n\n"
            "Arjuna looked across the battlefield. And his heart sank. 😔\n\n"
            "On the other side were his cousins. His teachers. His grandfather Bhishma. People he had grown up with. People he loved.\n\n"
            "\"How can I fight them?\" Arjuna whispered. He put down his bow.\n\n"
            "\"What is the point of winning a kingdom if I must kill my own family?\"\n\n"
            "Krishna looked at Arjuna with calm, knowing eyes. 🔵\n\n"
            "\"Arjuna, you are grieving for those who do not need your grief. The body dies, but the soul is eternal.\"\n\n"
            "\"You are a warrior. Your dharma — your duty — is to fight for what is right. To run away from duty is not kindness. It is fear wearing the mask of love.\"\n\n"
            "Arjuna was quiet for a long time.\n\n"
            "\"Do what is right,\" Krishna continued. \"Not for reward, not from anger — but because it IS right.\"\n\n"
            "Slowly, Arjuna picked up his bow. 🏹\n\n"
            "Not because he wasn't afraid. But because he understood:\n\n"
            "Some things must be done even when they are painful. Duty, truth, and courage — these are not always easy. But they are always necessary. 🌟"
        ),
        "think": "🤔 *Think About It!*\nArjuna had to make the hardest choice of his life. Have you ever had to do the right thing even when it was painful or scary? What did you choose?",
        "moral": "✨ *Today's Lesson:* Do what is right, not what is easy. Act from duty and love, not fear or anger."
    },
    {
        "id": 12,
        "title": "Rama's Hardest Choice",
        "age": "Ages 8–10 📚",
        "tradition": "Ramayana 🏹",
        "text": (
            "👑 The entire kingdom of Ayodhya was decorated with flowers and lamps. Tomorrow, Prince Rama would be crowned King!\n\n"
            "Rama smiled, touched by the love of his people. His wife Sita held his hand. His brother Lakshmana beamed with pride. 🌸\n\n"
            "But that night, his stepmother Kaikeyi went to the old King Dasharatha with a dark request.\n\n"
            "Long ago, the King had promised her two wishes. Now she was calling them in.\n\n"
            "\"Send Rama to the forest for fourteen years. Crown MY son Bharata instead.\"\n\n"
            "King Dasharatha wept. He begged. But a promise is a promise. ❤️‍🩹\n\n"
            "When Rama was told, the whole palace held its breath. Surely he would be angry? Surely he would refuse?\n\n"
            "Rama simply folded his hands. 🙏\n\n"
            "\"Father gave his word. I will go.\"\n\n"
            "\"But you are being robbed of your crown!\" Lakshmana cried.\n\n"
            "\"A crown means nothing if it is built on a broken promise,\" Rama said quietly.\n\n"
            "\"Our father's honor is worth more than a kingdom.\"\n\n"
            "Sita insisted on coming. Lakshmana refused to stay behind.\n\n"
            "They walked into the forest — no palace, no throne, no comfort.\n\n"
            "But Rama walked with peace in his heart.\n\n"
            "Because doing the right thing IS the reward — because you remain true to who you are. 🌿"
        ),
        "think": "🤔 *Think About It!*\nRama gave up something huge to keep his father's honor. Is there something right you gave up — because it wasn't fair to others? How did that feel?",
        "moral": "✨ *Today's Lesson:* Integrity means keeping your values even when it costs you something precious."
    },
    {
        "id": 13,
        "title": "The Merchant Who Let Go",
        "age": "Ages 8–10 📚",
        "tradition": "Jain ☮️",
        "text": (
            "💼 Sethji was the richest merchant in the city.\n\n"
            "He had a mansion, storerooms full of gold, chests of gems, and servants who ran at his every call. 💎🏛️\n\n"
            "But at night, Sethji could not sleep. He worried about his money. About thieves. About his business. About everything. 😰\n\n"
            "His mind never rested.\n\n"
            "One morning, he saw a Jain monk walking barefoot through the market. The monk had one simple robe and a small bowl.\n\n"
            "He was smiling — a deep, real smile.\n\n"
            "Sethji stopped him. \"Swamiji, you have nothing. Yet you seem so… at peace. How?\"\n\n"
            "The monk sat down in the dust and Sethji — a man who sat only on silk — sat beside him.\n\n"
            "\"You own everything,\" the monk said, \"but everything also owns you. Your gold never lets your mind rest.\"\n\n"
            "\"But if I give it all away, I'll have nothing!\" Sethji protested.\n\n"
            "\"What do you truly need?\" the monk asked gently.\n\n"
            "Sethji thought. Food. Shelter. Relationships. Health. None of those needed all that gold.\n\n"
            "\"I'm not saying give it all away. I'm saying: hold it lightly. Use it. But don't let it hold YOU.\"\n\n"
            "That night, Sethji donated half his wealth. He started a school. A hospital. A place for travelers to eat. 🏫🏥🍲\n\n"
            "He still had a business. But he slept. 😴\n\n"
            "He was still rich. But now he was free. ✨"
        ),
        "think": "🤔 *Think About It!*\nSethji confused having more with being happy. Is there something YOU have a lot of that you worry about? Would your life change if you held it lightly?",
        "moral": "✨ *Today's Lesson:* True wealth is inner peace. Hold your possessions lightly — they are tools, not your identity."
    },
    {
        "id": 14,
        "title": "Mirabai's Unstoppable Song",
        "age": "Ages 8–10 📚",
        "tradition": "Hindu 🕉️",
        "text": (
            "🎵 Princess Mirabai was born into royalty — jewels, servants, and a palace full of everything.\n\n"
            "But from childhood, she loved one thing above all else: singing to Lord Krishna.\n\n"
            "She would dance in the temple, eyes closed, heart open, completely lost in her devotion. 💙\n\n"
            "When she grew up and married, her in-laws expected her to stop.\n\n"
            "\"You embarrass us! A princess does not dance in public temples!\"\n\n"
            "They tried to stop her. They sent her a cup of poison.\n\n"
            "Mirabai drank it — with a prayer on her lips.\n\n"
            "She did not die. 🌸\n\n"
            "They sent her a basket with a deadly cobra.\n\n"
            "She opened it praying. The cobra had turned into a flower garland. 🌺\n\n"
            "The stories say Krishna protected her. Perhaps.\n\n"
            "Or perhaps — love that pure cannot be destroyed.\n\n"
            "Mirabai left the palace. She walked from temple to temple, singing.\n\n"
            "Common people — farmers, weavers, servants — gathered to hear her.\n\n"
            "Her songs were not complicated. They were honest and burning:\n\n"
            "\"Without You, I cannot live. Without You, nothing shines.\"\n\n"
            "She became one of India's greatest poet-saints.\n\n"
            "Not because she was powerful — but because she refused to let anyone silence what was true inside her heart. 🔥"
        ),
        "think": "🤔 *Think About It!*\nMirabai chose her truth over safety and approval. Is there something you believe deeply that others might not understand? How do you stay true to yourself?",
        "moral": "✨ *Today's Lesson:* Your inner truth — what you love, what you believe — is worth protecting. Don't let the world silence it."
    },
    {
        "id": 15,
        "title": "The Langar That Fed an Army",
        "age": "Ages 8–10 ",
        "tradition": "Sikh ",
        "text": (
            "Emperor Akbar had heard of Guru Amar Das — and the langar that fed everyone without distinction.\n\n"
            "He traveled to see for himself. His ministers whispered: \"Surely the Guru will make an exception for the Emperor?\"\n\n"
            "But the sevadars bowed and said:\n\n"
            "\"Pehle Pangat, Phir Sangat.\"\n\n"
            "🍲 First, you eat together. Then, you meet the Guru.\n\n"
            "Akbar saw farmers, merchants, the poor, the rich — all sitting on the floor, eating the same food. No high tables. No special treatment.\n\n"
            "His ministers shuffled uncomfortably.\n\n"
            "But Akbar removed his royal shoes, sat on the floor, and accepted a simple meal. 🙏\n\n"
            "He ate quietly among people he'd never shared a table with before.\n\n"
            "When he met Guru Amar Das, he said with awe:\n\n"
            "\"I have sat in many palaces. But I have never felt equality the way I did on that floor.\"\n\n"
            "\"That is the Guru's message,\" the Guru said. \"We are all the same before the One. No one sits higher. No one sits lower.\" ☝️🤲\n\n"
            "Akbar left changed — because he had felt, on that earthen floor, something a palace could never give him. 💛"
        ),
        "think": " *Think About It!*\nAkbar was powerful but still chose to be humble. When do you feel the temptation to think you're 'better' than someone else? What can help you remember that everyone deserves respect?",
        "moral": "✨ *Today's Lesson:* True greatness is not in rank or power — it is in treating every person as your equal."
    },
]


def load_tracker():
    if TRACKER_FILE.exists():
        with open(TRACKER_FILE) as f:
            return json.load(f)
    return {"last_sent_index": -1, "last_sent_date": None}


def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_today_story():
    tracker = load_tracker()
    today = str(date.today())

    if tracker["last_sent_date"] == today:
        print(f"Story already sent today ({today}). Skipping.")
        return None, None

    next_index = (tracker["last_sent_index"] + 1) % len(STORIES)
    story = STORIES[next_index]
    tracker["last_sent_index"] = next_index
    tracker["last_sent_date"] = today
    return story, tracker


def format_whatsapp_message(story):
    """Story title, body, think, and moral — no header/footer decorations."""
    return (
        f"📖 *{story['title']}*\n"
        f"🏷️ {story['tradition']}  |  {story['age']}\n\n"
        f"{story['text']}\n\n"
        f"{story['think']}\n\n"
        f"{story['moral']}"
    )


def send_whatsapp_message(text):
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    response = requests.post(
        url,
        auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        data={"From": FROM_NUMBER, "To": TO_NUMBER, "Body": text}
    )
    return response


def main():
    story, tracker = get_today_story()
    if story is None:
        return

    message = format_whatsapp_message(story)

    print(f"Sending story #{tracker['last_sent_index'] + 1}: {story['title']} ({len(message)} chars)")

    response = send_whatsapp_message(message)
    if response.status_code not in (200, 201):
        print(f"❌ Failed to send. Status: {response.status_code}")
        print(response.text)
        return

    print("✅ Story sent successfully!")
    save_tracker(tracker)


if __name__ == "__main__":
    main()
