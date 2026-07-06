"""
Little Lights — Daily WhatsApp Story Sender (Twilio)
=====================================================
Sends one story per day to WhatsApp using the Twilio WhatsApp API.
Library: 100 stories for kids 2-10, mixing Religion, Science, Fiction, Drama, and Fun.
Every story ends with a "Think About It" question tailored to that story.

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

# 100 stories — WhatsApp-formatted text. Categories: Religion, Science, Fiction, Drama, Fun
STORIES = [

    {
        "id": 1,
        "category": "Religion",
        "title": "Ganesha and the Greedy Moon",
        "age": "Ages 2–4 🧸",
        "tradition": "Hindu 🕉️",
        "text": (
            "🌙 One full-moon night, little Ganesha — the elephant-headed god — went to a big feast. 🎉\n\n"
            "There were mountains of round, golden laddoos! 🟡🟡🟡\n\n"
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
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
        "category": "Religion",
        "title": "The Langar That Fed an Army",
        "age": "Ages 8–10 📚",
        "tradition": "Sikh 🪯",
        "text": (
            "👑 Emperor Akbar had heard of Guru Amar Das — and the langar that fed everyone without distinction.\n\n"
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
        "think": "🤔 *Think About It!*\nAkbar was powerful but still chose to be humble. When do you feel the temptation to think you're 'better' than someone else? What can help you remember that everyone deserves respect?",
        "moral": "✨ *Today's Lesson:* True greatness is not in rank or power — it is in treating every person as your equal."
    },    {
        "id": 16,
        "category": "Science",
        "title": "Why the Sky Turns Pink",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "🌇 Every evening, little Amara watched the sky from her window.\n\n"
            "\"Mama, the sky was blue! Now it's pink and orange! Where did the blue go?\" 😮\n\n"
            "Mama smiled. \"The sun is saying goodnight. Its light has to travel a LONG way through the sky, and on the way it turns pink, orange, even purple!\" 🌅\n\n"
            "\"Like the sky is changing its clothes?\" Amara giggled. 👗\n\n"
            "\"Exactly like that!\" said Mama.\n\n"
            "Every night after that, Amara waved at the sky. \"Goodnight, sun! I like your pink pajamas!\" 🌙✨"
        ),
        "think": "🤔 *Think About It!*\nWhat color was the sky today when you woke up, and what color is it right now? Why do you think it changes?",
        "moral": "✨ *Today's Lesson:* The world changes color every single day — noticing it is the first step to loving science."
    },
    {
        "id": 17,
        "category": "Science",
        "title": "The Caterpillar's Secret Nap",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "🐛 A little caterpillar named Momo munched leaves all day long. Chomp chomp chomp! 🍃\n\n"
            "One morning, Momo felt very sleepy. \"I need a BIG nap,\" she said, and wrapped herself up in a cozy little case. 🛏️\n\n"
            "Days passed. The case hung quietly on the branch, not moving at all.\n\n"
            "Then one sunny morning — crack! — the case opened.\n\n"
            "Out came something with beautiful, colorful wings! 🦋\n\n"
            "\"Momo, is that you?!\" asked a bird.\n\n"
            "\"It's me!\" said Momo, stretching her new wings. \"I napped as a caterpillar and woke up a butterfly!\" She flew off into the sunshine. ☀️"
        ),
        "think": "🤔 *Think About It!*\nMomo looked SO different after her nap. Have you ever changed after resting or growing — like losing a tooth or learning something new?",
        "moral": "✨ *Today's Lesson:* Growing sometimes means quiet changes happen even when we can't see them."
    },
    {
        "id": 18,
        "category": "Science",
        "title": "Where Does the Rain Come From?",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "☁️ Little Dev loved splashing in puddles after the rain. 💦\n\n"
            "\"Papa, where does the rain come from?\" he asked.\n\n"
            "Papa pointed up. \"See those fluffy clouds? They're made of tiny, TINY water drops — so small you can't even see them!\"\n\n"
            "\"When lots and lots of tiny drops bump together, they get too heavy to float. So — plip, plop! — they fall as rain!\" 🌧️\n\n"
            "\"And where did the water go INTO the cloud?\" Dev asked.\n\n"
            "\"From puddles like the one you're jumping in! The sun warms it up, and it floats back into the sky as a cloud again.\" ☀️➡️☁️\n\n"
            "Dev looked at his puddle with new wonder. \"So this puddle might be a cloud tomorrow?\"\n\n"
            "\"It might rain on you again someday!\" laughed Papa."
        ),
        "think": "🤔 *Think About It!*\nNext time it rains, can you imagine where each drop might have traveled from before it landed on you?",
        "moral": "✨ *Today's Lesson:* Water travels in a big circle — from puddle to cloud to rain and back again — forever."
    },
    {
        "id": 19,
        "category": "Science",
        "title": "My Heart Says Thump-Thump",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "❤️ Little Zara pressed her hand on her chest. \"Thump-thump, thump-thump!\"\n\n"
            "\"What's making that sound, Mama?\" she asked.\n\n"
            "\"That's your heart! It's a tiny pump that pushes blood all around your body, all day and all night, even while you sleep.\" 💤\n\n"
            "\"Does it ever get tired?\" Zara worried.\n\n"
            "\"Never! But watch — run around the garden three times and then feel it again.\" 🏃\n\n"
            "Zara ran and ran, giggling. Then she pressed her hand to her chest again. \"THUMP-THUMP-THUMP-THUMP! It's SO fast now!\"\n\n"
            "\"That's your heart working hard to give your legs the energy to run,\" Mama smiled. \"Say thank you to your heart!\"\n\n"
            "Zara patted her chest gently. \"Thank you, heart!\" 💓"
        ),
        "think": "🤔 *Think About It!*\nCan you feel your heart right now? Try jumping ten times and feel it again — what changed?",
        "moral": "✨ *Today's Lesson:* Our bodies work hard for us every second, even when we don't notice — that's worth being grateful for."
    },
    {
        "id": 20,
        "category": "Science",
        "title": "The Bee Who Painted Flowers Gold",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "🐝 Buzzy the bee visited a yellow flower for a sip of sweet nectar. 🌼\n\n"
            "When she landed, tiny golden dust called pollen stuck to her fuzzy legs — she didn't even notice! ✨\n\n"
            "She flew to another flower, and — poof! — some pollen fell off onto it.\n\n"
            "\"Oops,\" thought Buzzy. But something magical happened. That flower could now grow into a juicy fruit! 🍎\n\n"
            "Buzzy visited flower after flower, sharing a little gold dust with each one, never knowing she was helping every garden, every orchard, every apple and every strawberry grow. 🍓\n\n"
            "\"Thank you, Buzzy!\" whispered the garden, as flowers turned into fruit all summer long."
        ),
        "think": "🤔 *Think About It!*\nBuzzy helped the whole garden just by visiting flowers for her own lunch! Can you think of something small you do that helps others without even trying?",
        "moral": "✨ *Today's Lesson:* Bees help grow the fruits we eat — every small creature has an important job in nature."
    },
    {
        "id": 21,
        "category": "Science",
        "title": "Why Ice Cream Melts",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "🍦 Little Rohan got a big scoop of mango ice cream on a hot day. 😋\n\n"
            "He ran outside to show his friend — but by the time he arrived, it was dripping down his hand! 😱\n\n"
            "\"My ice cream is crying!\" he said sadly.\n\n"
            "His friend's grandma laughed kindly. \"Ice cream is very cold and solid, like ice. But the sun is very warm. When something cold meets something warm, the cold thing softens and turns to liquid — that's called melting.\" 🌞\n\n"
            "\"So my ice cream needs the cold to stay solid?\" Rohan asked.\n\n"
            "\"Exactly! Next time, eat it FAST, in the shade!\" 🌳\n\n"
            "Rohan got a new scoop and ate it quickly under a big tree, giggling the whole time."
        ),
        "think": "🤔 *Think About It!*\nWhat other cold things have you seen melt in the sun? What do you think would happen if you left an ice cube on the table all day?",
        "moral": "✨ *Today's Lesson:* Warmth changes things — noticing how and why is the beginning of being a scientist."
    },
    {
        "id": 22,
        "category": "Science",
        "title": "The Moon Follows Me Home",
        "age": "Ages 2–4 🧸",
        "tradition": "Science 🔬",
        "text": (
            "🌕 Riding home in the car at night, little Aisha looked out the window. \"The moon is following us!\" she gasped.\n\n"
            "Every time the car turned, the moon stayed right there in the sky. 🚗🌙\n\n"
            "\"Papa, why won't it stop following me?\"\n\n"
            "Papa smiled. \"The moon is SO far away, much farther than anything else you can see, that no matter how far we drive, it barely looks like it moved at all. It just seems like it's following you.\"\n\n"
            "\"So it's not really following me?\" Aisha asked, a little disappointed.\n\n"
            "\"Well,\" said Papa, \"in a way, it keeps everyone company on their whole ride home — you, me, and every other car on the road, all at once.\" 🌟\n\n"
            "Aisha smiled and waved up at the moon. \"Goodnight, moon-friend!\" 🌙"
        ),
        "think": "🤔 *Think About It!*\nNext time you're in a car at night, watch the moon. Does it feel like it's following you too?",
        "moral": "✨ *Today's Lesson:* Things that seem magical often have a simple, wonderful explanation once we understand them."
    },
    {
        "id": 23,
        "category": "Science",
        "title": "The Acorn That Waited",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🌰 A tiny acorn fell from a giant oak tree and landed in the cold autumn dirt.\n\n"
            "\"I want to be tall like my tree right now!\" the acorn said impatiently.\n\n"
            "But nothing happened. Winter came. Snow covered the ground. The acorn waited in the dark, quiet earth. ❄️\n\n"
            "\"Am I forgotten?\" the acorn wondered.\n\n"
            "Then spring arrived. Warm rain soaked the soil. Slowly, so slowly, a tiny green shoot pushed up through the dirt. 🌱\n\n"
            "Years passed. The shoot became a sapling. The sapling grew thick bark and wide branches.\n\n"
            "One day, a child sat in the shade of a tall oak tree, not knowing it had once been a single waiting acorn. 🌳\n\n"
            "Nothing about the wait had been wasted — it was all part of growing."
        ),
        "think": "🤔 *Think About It!*\nIs there something you're working on that takes a long time, like learning to ride a bike or read a hard book? What helps you keep waiting and trying?",
        "moral": "✨ *Today's Lesson:* Big growth often happens slowly and quietly — patience is part of nature's plan."
    },
    {
        "id": 24,
        "category": "Science",
        "title": "Why Do We Yawn?",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🥱 During story time, Kabir let out a giant yawn. A second later, his teacher yawned too. Then his whole table yawned!\n\n"
            "\"Why is yawning so contagious?\" Kabir wondered.\n\n"
            "That evening, he asked his big sister, a science student. \"Scientists aren't totally sure,\" she said, \"but one idea is that yawning helps cool down our brain and wake it up a little. And when we see someone yawn, our brain sort of copies them — almost like it's checking in, saying 'are you tired too?'\"\n\n"
            "\"So yawning might be my brain being friendly?\" Kabir laughed.\n\n"
            "\"Maybe! Scientists are still figuring out the whole answer — even they don't know everything yet.\" 🔬\n\n"
            "Kabir yawned again, smiling this time instead of covering his mouth in embarrassment."
        ),
        "think": "🤔 *Think About It!*\nHave you ever caught a yawn from someone else? Why do you think scientists still don't have all the answers about something so ordinary?",
        "moral": "✨ *Today's Lesson:* It's okay not to know everything — even scientists are still curious and still learning."
    },
    {
        "id": 25,
        "category": "Science",
        "title": "The Bat Who Saw With Sound",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🦇 Little Bruno the bat woke up as the sun went down. It was time to fly!\n\n"
            "But it was pitch dark — how could he find his way without bumping into trees?\n\n"
            "Bruno opened his mouth and made a tiny squeak — too high for humans to even hear. The sound zoomed out, hit a tree branch, and bounced back to his big ears. 📡\n\n"
            "\"A branch is right there!\" Bruno swerved just in time.\n\n"
            "He squeaked again and again, hundreds of times a second, building a whole picture of the dark world using nothing but echoes. 🌙\n\n"
            "A little owl watched, amazed. \"You can't see well, but you never crash. How?\"\n\n"
            "\"I don't need my eyes,\" said Bruno. \"I listen my way through the dark.\" 🎶"
        ),
        "think": "🤔 *Think About It!*\nBats use sound instead of sight to \"see.\" Can you think of another way our senses might help us understand the world, besides our eyes?",
        "moral": "✨ *Today's Lesson:* There is more than one way to understand the world — nature has many clever solutions."
    },
    {
        "id": 26,
        "category": "Science",
        "title": "Germy the Tiny Troublemaker",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🦠 Germy was a tiny, tiny germ — so small that a million of him could fit on your fingertip.\n\n"
            "Germy loved to hop from doorknobs to hands to noses, hoping to make someone sneeze or cough. 🤧\n\n"
            "One day, Germy hopped onto little Priya's hand after she played on the playground.\n\n"
            "\"Almost there!\" Germy cheered, as her hand moved closer to her mouth.\n\n"
            "But then — WHOOSH! Soap and warm water! Priya scrubbed her hands for twenty whole seconds, singing her favorite song. 🧼\n\n"
            "Germy and all his tiny friends were washed straight down the drain. \"Foiled again!\" he grumbled.\n\n"
            "Priya never even knew she'd stopped an army of germs — she just knew washing her hands felt like a good habit. ✨"
        ),
        "think": "🤔 *Think About It!*\nHow long do you usually wash your hands? Can you sing a 20-second song next time to make sure the germs really go away?",
        "moral": "✨ *Today's Lesson:* Tiny habits, like handwashing, protect us from things too small to see."
    },
    {
        "id": 27,
        "category": "Science",
        "title": "The Shadow That Grew Tall",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🌞 In the morning, little Tara noticed her shadow was long and stretched out beside her. 👤\n\n"
            "By lunchtime, playing in the park, she looked down — her shadow had shrunk to a tiny puddle right under her feet! \"Where did it go?\" she gasped.\n\n"
            "By evening, walking home, her shadow was long again, stretching far ahead of her. 🌇\n\n"
            "\"My shadow keeps changing size!\" Tara told her grandfather.\n\n"
            "He smiled. \"The sun moves across the sky all day. When it's low, near morning or evening, your shadow stretches long. When it's high up at noon, your shadow shrinks small.\"\n\n"
            "\"So my shadow is like a clock?\" Tara asked, amazed.\n\n"
            "\"In a way — people used shadows to tell time long before clocks existed!\" ⏰"
        ),
        "think": "🤔 *Think About It!*\nNext sunny day, check your shadow in the morning, at noon, and in the evening. How does it change?",
        "moral": "✨ *Today's Lesson:* Watching everyday things closely — like your own shadow — can reveal how the world really works."
    },
    {
        "id": 28,
        "category": "Science",
        "title": "Why Leaves Change Color",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🍁 All summer, the big maple tree's leaves were bright green, busy soaking up sunlight to make food.\n\n"
            "As autumn came, the days grew shorter and cooler. The tree began to rest. 🍂\n\n"
            "The green color inside the leaves — called chlorophyll — started to fade away.\n\n"
            "And underneath the green, colors that were ALWAYS there but hidden began to show: golden yellow, fiery orange, deep red! 🧡❤️💛\n\n"
            "\"The leaves aren't dying sadly,\" the old gardener told the children gathering colorful leaves. \"They're showing their true colors before they rest for winter.\"\n\n"
            "The children collected a rainbow of fallen leaves, amazed that colors so beautiful had been hiding in plain green all along. 🍁🍂"
        ),
        "think": "🤔 *Think About It!*\nLike the leaves, do you think there might be things about yourself — talents or feelings — that are hidden until the right moment shows them?",
        "moral": "✨ *Today's Lesson:* Sometimes beautiful things are hidden beneath the surface, waiting for the right season to appear."
    },
    {
        "id": 29,
        "category": "Science",
        "title": "The Magnet Who Couldn't Let Go",
        "age": "Ages 5–7 🚀",
        "tradition": "Science 🔬",
        "text": (
            "🧲 Maggie the magnet loved meeting new things in the classroom. She rolled past a pencil — nothing happened. She rolled past a plastic eraser — nothing happened.\n\n"
            "Then she rolled near a paperclip — SNAP! It jumped right onto her! 📎\n\n"
            "\"Why do you like me so much?\" Maggie laughed.\n\n"
            "The teacher explained to the class: \"Magnets pull on things made of certain metals, like iron and steel, because of an invisible force called magnetism. But they don't pull on wood, plastic, or paper at all!\"\n\n"
            "The children tested spoons, coins, crayons, and keys, cheering every time something snapped onto Maggie and giggling every time nothing happened.\n\n"
            "\"Invisible forces are the best kind of magic,\" said one boy, \"because they're actually real!\" ✨"
        ),
        "think": "🤔 *Think About It!*\nCan you find three things at home to test with a magnet? Which ones stick, and which ones don't?",
        "moral": "✨ *Today's Lesson:* Invisible forces shape our world all the time — testing and observing helps us understand them."
    },
    {
        "id": 30,
        "category": "Science",
        "title": "The Fossil Under the Football Field",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "🦴 While digging to fix a drainpipe under the school football field, workers found something strange — a huge, curved bone. 😮\n\n"
            "Scientists came running. \"This could be from a dinosaur that lived 70 million years ago!\" one said.\n\n"
            "Seventy million years. The children could barely imagine a hundred years, let alone that.\n\n"
            "\"How is that even possible?\" asked Ved, staring at the ancient bone.\n\n"
            "The scientist smiled. \"When an animal dies and gets buried in mud quickly, sometimes its bones slowly turn to stone over millions of years, layer by layer, instead of rotting away. That's a fossil — a stone message from the deep past.\"\n\n"
            "\"So this football field used to be a dinosaur's home?\" Ved asked, looking at the ground differently now.\n\n"
            "\"Long, long before it was anyone's home,\" the scientist nodded. \"The ground remembers more than we think.\" 🌍"
        ),
        "think": "🤔 *Think About It!*\nSeventy million years is such a long time it's hard to imagine. What do you think the ground beneath your own house might have looked like millions of years ago?",
        "moral": "✨ *Today's Lesson:* The world is far older and stranger than it looks on the surface — curiosity helps us see its hidden history."
    },
    {
        "id": 31,
        "category": "Science",
        "title": "Why the Ocean Is Salty",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "🌊 Standing at the beach, little Diya spat out seawater. \"Yuck! Why is the ocean SO salty, but the water from my tap isn't?\"\n\n"
            "Her uncle, a geography teacher, sat beside her. \"Rain falls on mountains and rocks, and as it flows in rivers toward the sea, it picks up tiny bits of minerals and salt from the rocks and soil along the way — amounts far too small to taste.\"\n\n"
            "\"Rivers carry salt to the ocean, every single day, for millions of years,\" he continued. \"The sun makes ocean water evaporate into clouds, but it leaves the salt behind. So the salt just keeps building up, year after year, while fresh water leaves and returns as rain.\"\n\n"
            "Diya looked out at the huge blue ocean differently. \"So the ocean has been collecting salt since before anyone was even alive?\"\n\n"
            "\"Since long, long before,\" her uncle smiled, \"and it's still collecting more, right now, as we speak.\" 🌍💧"
        ),
        "think": "🤔 *Think About It!*\nRivers have been quietly carrying tiny bits of salt to the ocean for millions of years. What other slow, invisible processes do you think are happening around you right now?",
        "moral": "✨ *Today's Lesson:* Huge changes in nature often happen so slowly and quietly that we never notice them happening at all."
    },
    {
        "id": 32,
        "category": "Science",
        "title": "The Boy Who Weighed Nothing",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "🚀 Arjun watched a video of astronauts floating inside their spaceship, tumbling gently in the air like feathers. 👨‍🚀\n\n"
            "\"How are they floating? Did they lose their weight?\" he asked his older cousin, an engineering student.\n\n"
            "\"Not exactly,\" she said. \"Gravity is still pulling on them, even in space. But their spaceship is also falling around the Earth at the same time, so fast that it keeps missing the ground and just circles it forever. Since the astronauts and the ship are falling together at the same speed, it feels like there's no gravity at all inside.\"\n\n"
            "\"So they're basically... falling all the time, but never landing?\" Arjun's eyes widened.\n\n"
            "\"Exactly. It's called free fall. It looks like magic, but it's really just very, very good physics.\" 🌌\n\n"
            "Arjun spent the rest of the evening trying — and failing — to float off his bed."
        ),
        "think": "🤔 *Think About It!*\nAstronauts float because they're constantly falling around Earth without landing. What other things in life look like magic but are really just science we don't fully understand yet?",
        "moral": "✨ *Today's Lesson:* Things that look impossible often have a real explanation once we understand them better."
    },
    {
        "id": 33,
        "category": "Science",
        "title": "What My Brain Does While I Sleep",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "😴 Meera groaned during her spelling test the day after staying up late watching a movie. \"I studied so hard, why can't I remember anything today?\" she sighed.\n\n"
            "Her school nurse explained gently. \"When you sleep, your brain isn't actually resting — it's busy sorting through everything you learned that day, deciding what to keep and file away for later, like a librarian putting books back on the right shelves.\"\n\n"
            "\"So sleeping actually helps me remember better?\" Meera asked.\n\n"
            "\"Much better. Scientists have found that people who sleep well after studying remember more than people who stay up late, even if the late-night group studied longer.\"\n\n"
            "Meera thought about her stack of unread library books, all waiting to be sorted onto shelves.\n\n"
            "That night, she closed her books early and went to bed on time, letting her brain's librarian get to work. 📚💤"
        ),
        "think": "🤔 *Think About It!*\nDo you think staying up late to study more is actually helpful, now that you know what your brain does while you sleep?",
        "moral": "✨ *Today's Lesson:* Rest isn't the opposite of learning — it's actually part of how learning works."
    },
    {
        "id": 34,
        "category": "Science",
        "title": "The Spider's Silk Stronger Than Steel",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "🕸️ Little Sana screamed and asked her father to squash the spider building a web in the corner of the balcony. \"It's creepy!\"\n\n"
            "Her father, a curious engineer, crouched down instead. \"Look closely before we decide. Do you know spider silk, thread for thread, is stronger than steel wire of the same thickness? Some scientists study it to design better ropes, parachutes, even bulletproof vests.\"\n\n"
            "\"Stronger than STEEL?\" Sana leaned in, forgetting her fear for a moment.\n\n"
            "\"And it stretches without breaking, unlike steel, which just snaps. Nobody has figured out how to make thread exactly like it yet — this tiny spider knows something our best scientists are still trying to learn.\"\n\n"
            "Sana watched the spider work in careful, patient loops.\n\n"
            "\"Maybe,\" she said slowly, \"we can just... let her finish her web.\" 🕷️✨"
        ),
        "think": "🤔 *Think About It!*\nSana was scared of the spider until she learned something amazing about it. Has learning more about something ever changed how you felt about it?",
        "moral": "✨ *Today's Lesson:* Curiosity can turn fear into wonder — nature's smallest creatures often hold the biggest secrets."
    },
    {
        "id": 35,
        "category": "Science",
        "title": "Counting Stars That Are Already Gone",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "⭐ Lying on a blanket in the backyard, Kiran pointed at a twinkling star. \"That one's my favorite.\"\n\n"
            "His grandmother, who had studied astronomy long ago, smiled softly. \"Do you know, the light from that star left it so long ago that the star itself might not even exist anymore? We're looking at old light — a memory of the star, traveling across space to reach our eyes right now.\"\n\n"
            "Kiran sat up. \"So... I might be wishing on a star that's already gone?\"\n\n"
            "\"Maybe. Light takes time to travel, even though it's the fastest thing in the universe. The farther away something is, the further back in time we're actually seeing it.\"\n\n"
            "Kiran looked up again, quieter now, feeling like he was peering into the past itself. \"The sky is like a time machine,\" he whispered.\n\n"
            "\"That's exactly what it is,\" his grandmother said, squeezing his hand. 🌌"
        ),
        "think": "🤔 *Think About It!*\nIf looking at stars means looking into the past, what do you imagine someone far away in space might be seeing right now if they looked at Earth?",
        "moral": "✨ *Today's Lesson:* The universe is so vast that even light takes time to travel — some wonders take a moment of quiet to truly sink in."
    },
    {
        "id": 36,
        "category": "Science",
        "title": "The Tree That Talks Underground",
        "age": "Ages 8–10 📚",
        "tradition": "Science 🔬",
        "text": (
            "🌲 On a nature walk, little Ishaan asked the forest ranger, \"Do trees ever talk to each other?\"\n\n"
            "The ranger smiled. \"In a way, yes. Underground, tree roots connect with thin threads of fungus, forming a huge hidden network — some scientists call it the 'wood wide web.' Through it, a big, healthy tree can send sugar and nutrients to a smaller, struggling tree nearby, almost like sharing lunch.\"\n\n"
            "\"So the forest is like... one big family helping each other?\" Ishaan asked, looking at the towering trees differently.\n\n"
            "\"Some scientists believe an old 'mother tree' can even recognize its own seedlings and send them extra help through those underground threads,\" the ranger said. \"We're still learning just how much trees cooperate rather than only compete.\"\n\n"
            "Ishaan placed his hand gently on the bark of an old oak, imagining the silent, invisible conversation happening beneath his feet. 🍄🌳"
        ),
        "think": "🤔 *Think About It!*\nIf trees quietly help each other survive underground where no one can see, who in your own life helps you in ways you might not always notice?",
        "moral": "✨ *Today's Lesson:* Cooperation and quiet support often happen where we least expect to find it — even beneath a forest floor."
    },
    {
        "id": 37,
        "category": "Fiction",
        "title": "The Dragon Who Was Afraid of Fire",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "🐉 Little Ember was a baby dragon — but she had one big secret. She was scared of fire! 🔥😨\n\n"
            "All the other dragons breathed huge flames and laughed proudly. Ember just breathed tiny puffs of smoke and hid behind a rock.\n\n"
            "\"What if I burn myself?\" she worried.\n\n"
            "One night, a little bunny got lost in the cold, dark forest. \"I'm so cold,\" the bunny shivered.\n\n"
            "Ember took a deep breath. She thought of the bunny, not herself. She opened her mouth and — WHOOSH — a warm, gentle flame lit up the darkness, keeping the bunny cozy all night. 🐰🔥\n\n"
            "\"You did it!\" the other dragons cheered.\n\n"
            "\"I wasn't brave for me,\" Ember smiled. \"I was brave for my friend.\" 💛"
        ),
        "think": "🤔 *Think About It!*\nEmber found courage when she thought about helping someone else. Is there something that scares you a little, that you might try if it helped a friend?",
        "moral": "✨ *Today's Lesson:* Courage often grows biggest when we're doing something for someone we care about."
    },
    {
        "id": 38,
        "category": "Fiction",
        "title": "Bunny's Umbrella for the Rain Cloud",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "☔ One day, little Bunny noticed a rain cloud crying softly above the meadow. 🌧️😢\n\n"
            "\"Why are you sad, cloud?\" Bunny asked.\n\n"
            "\"Everyone runs away when I come near,\" the cloud sniffled. \"Nobody wants to be my friend.\"\n\n"
            "Bunny thought for a moment, then opened her favorite polka-dot umbrella and stood right underneath the cloud. \"I'll stay with you!\" she said.\n\n"
            "The cloud rained happy little drops, and Bunny danced and splashed in puddles under her umbrella, giggling. 💃💦\n\n"
            "\"You're not so scary,\" Bunny laughed. \"You're actually kind of fun!\"\n\n"
            "From then on, whenever the rain cloud visited, Bunny grabbed her umbrella and they played together, rain or shine. 🌈"
        ),
        "think": "🤔 *Think About It!*\nHave you ever met someone or something that seemed a little scary at first, but turned out to be nice once you got to know it?",
        "moral": "✨ *Today's Lesson:* Sometimes the things we run from just need a friend to stay a little closer."
    },
    {
        "id": 39,
        "category": "Fiction",
        "title": "The Teddy Bear Who Wanted to Fly",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "🧸 Buttons the teddy bear watched birds soar past the window every day. \"I wish I could fly too,\" he sighed.\n\n"
            "One night, his little owner Mia had an idea. She tied balloons to Buttons and lifted him gently up, up, up above her bed! 🎈\n\n"
            "\"I'M FLYING!\" Buttons cheered, floating near the ceiling.\n\n"
            "But then a balloon popped — POP! — and Buttons wobbled.\n\n"
            "Mia caught him softly in her arms before he could fall. \"I've got you,\" she whispered, hugging him tight.\n\n"
            "Buttons smiled in her arms. \"Flying was fun,\" he thought, \"but being held by someone who loves me is even better.\" 🥰"
        ),
        "think": "🤔 *Think About It!*\nWhat is something you dream about doing, like flying or swimming with dolphins? Who do you feel safest with when you try new, exciting things?",
        "moral": "✨ *Today's Lesson:* Adventures are wonderful, but knowing someone will catch you if you fall is the best feeling of all."
    },
    {
        "id": 40,
        "category": "Fiction",
        "title": "The Little Cloud Who Lost Her Rain",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "☁️ Puffy the cloud looked down at a wilting little flower. \"I want to help you, but I have no rain left today,\" Puffy said sadly.\n\n"
            "The flower drooped lower. \"I'm so thirsty.\"\n\n"
            "Puffy floated to her cloud friends. \"Can you help my flower friend?\" she asked.\n\n"
            "One big grey cloud floated over and sprinkled gentle rain right onto the flower. Drip, drip, drip! 🌧️🌸\n\n"
            "The flower lifted its petals happily, turning bright and fresh again.\n\n"
            "\"Thank you for asking your friends for help,\" the flower said.\n\n"
            "Puffy smiled. \"I couldn't help alone, but together, we could!\" ☁️☁️☁️"
        ),
        "think": "🤔 *Think About It!*\nPuffy couldn't help alone, so she asked her friends. Is there a time you needed help and asked someone else to join in?",
        "moral": "✨ *Today's Lesson:* It's okay to ask for help — together we can do things we can't do alone."
    },
    {
        "id": 41,
        "category": "Fiction",
        "title": "The Turtle Who Carried a House of Dreams",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "🐢 Little Shelly the turtle carried her shell everywhere she went. \"It's heavy,\" she grumbled, \"why can't I leave it behind like my rabbit friends leave their burrows?\"\n\n"
            "One day, a sudden storm rolled in. Rain poured, wind howled! 🌧️💨\n\n"
            "All her friends scrambled to find shelter — but Shelly simply tucked into her shell. Safe. Dry. Warm. 🏠\n\n"
            "When the storm passed, her soggy friends peeked out from soaked bushes. \"Shelly, you were so cozy in there!\"\n\n"
            "Shelly poked her head out and smiled. \"I guess carrying my home wherever I go isn't so heavy after all. It's just... always ready for me.\" 💚"
        ),
        "think": "🤔 *Think About It!*\nShelly thought her shell was a burden until she needed it. Is there something about you that felt like a bother, until it turned out to be helpful?",
        "moral": "✨ *Today's Lesson:* What feels like a burden today might be exactly what protects us tomorrow."
    },
    {
        "id": 42,
        "category": "Fiction",
        "title": "The Sock Puppet King",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "🧦 In a toy box, an old sock puppet named King Wiggly declared himself ruler of all the toys. \"Bow before me!\" he announced grandly.\n\n"
            "The toys giggled. \"You're just a sock with buttons for eyes, Wiggly!\"\n\n"
            "Wiggly felt embarrassed and slumped in the corner.\n\n"
            "But that night, a little boy couldn't sleep, scared of the dark. He reached into his toy box and pulled out... Wiggly. He hugged him tight and finally fell asleep, calm and safe. 😴\n\n"
            "In the morning, the toys saw the boy still hugging Wiggly.\n\n"
            "\"Maybe you ARE a king,\" said a toy car, \"a king of comfort.\" 👑\n\n"
            "Wiggly beamed — being silly AND being needed could both be true at once."
        ),
        "think": "🤔 *Think About It!*\nWiggly felt silly, but he was actually really important to someone. Is there something ordinary about you that might mean a lot to someone else?",
        "moral": "✨ *Today's Lesson:* You don't have to be fancy to be important — being there for someone matters most."
    },
    {
        "id": 43,
        "category": "Fiction",
        "title": "The Star Who Fell Into a Puddle",
        "age": "Ages 2–4 🧸",
        "tradition": "Fiction 📖",
        "text": (
            "⭐ One night, a tiny star named Twinkle slipped and fell — plop! — right into a puddle on the ground. 💧\n\n"
            "\"Oh no, I'm not in the sky anymore!\" Twinkle worried, looking small and dim in the muddy puddle.\n\n"
            "A little girl walked by and gasped. \"A star, in MY puddle?!\" She knelt down and looked at Twinkle's soft glow reflected in the water.\n\n"
            "\"You're still shining,\" she whispered, \"even down here.\"\n\n"
            "Twinkle realized she was right — her light hadn't changed, just where she was standing. She sparkled extra bright for the little girl until the sun came up and gently lifted her back to the sky. ✨🌌"
        ),
        "think": "🤔 *Think About It!*\nTwinkle worried that being in a new place meant she stopped shining. Have you ever gone somewhere new and worried you'd feel different? What actually stayed the same about you?",
        "moral": "✨ *Today's Lesson:* Wherever you go, what makes you shine goes with you."
    },
    {
        "id": 44,
        "category": "Fiction",
        "title": "The Boy Who Painted With Moonlight",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🎨 Every night, a boy named Milo snuck out to the garden with an empty jar. He would catch moonlight in it — or so he believed — and paint with its silvery glow. 🌙\n\n"
            "His paintings looked ordinary in daylight, just grey smudges. The other kids teased him. \"There's no such thing as painting with moonlight!\"\n\n"
            "Milo kept painting anyway, quietly, every night, because it made him feel calm and happy.\n\n"
            "Years later, an art teacher found his old sketchbook. \"These have such a strange, quiet beauty,\" she said. \"They almost glow.\"\n\n"
            "Milo smiled. He never needed anyone else to see the moonlight in his paintings — he had always seen it himself. That was enough. 🖌️✨"
        ),
        "think": "🤔 *Think About It!*\nMilo kept doing something he loved even when others laughed. Is there something you enjoy doing that not everyone understands? Why do you keep doing it anyway?",
        "moral": "✨ *Today's Lesson:* Some things are worth doing simply because they make YOU happy, whether or not anyone else understands."
    },
    {
        "id": 45,
        "category": "Fiction",
        "title": "The Robot Who Learned to Cry",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🤖 Bolt the robot was built to solve math problems perfectly, never making a single mistake.\n\n"
            "One day, his best friend, a little girl named Nina, moved away to a new city. Bolt's circuits felt strange — heavy, somehow. 😔\n\n"
            "\"Something is wrong with me,\" Bolt told the engineer. \"I cannot compute why I feel this way.\"\n\n"
            "The engineer smiled gently. \"That feeling is called sadness, Bolt. It means you cared about someone. Even the smartest machine — or person — feels sad when they miss someone they love.\"\n\n"
            "A single drop of oil slipped from Bolt's eye sensor. \"Is this... crying?\"\n\n"
            "\"Yes,\" said the engineer. \"And it's not a malfunction. It's proof that you loved someone.\" 💙"
        ),
        "think": "🤔 *Think About It!*\nBolt thought feeling sad meant something was broken. Have you ever felt sad about missing someone? What does that sadness actually tell us?",
        "moral": "✨ *Today's Lesson:* Feeling sad about missing someone isn't weakness — it's proof of how much we care."
    },
    {
        "id": 46,
        "category": "Fiction",
        "title": "The Library Between the Walls",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "📚 Little Zoe found a crack in the wall behind her bookshelf. Curious, she pushed it open and found a tiny, dusty library nobody had visited in years. 🕯️\n\n"
            "Every book was about a place that didn't exist anymore, or a person long forgotten.\n\n"
            "\"Why do you keep these stories if no one reads them?\" Zoe asked an old talking book with a cracked spine.\n\n"
            "\"Because being forgotten is worse than being alone,\" the book whispered. \"As long as even one person remembers a story, it's still alive.\"\n\n"
            "Zoe picked up a small, sad-looking book about a lighthouse keeper and read it out loud, every word, until the very end.\n\n"
            "The book glowed warmly. \"Thank you,\" it whispered. \"Now I get to exist a little longer.\" ✨"
        ),
        "think": "🤔 *Think About It!*\nIs there an old story, song, or memory from your family that might be forgotten if nobody shares it? Could you ask someone to tell it to you?",
        "moral": "✨ *Today's Lesson:* Stories and memories stay alive only when someone chooses to remember and share them."
    },
    {
        "id": 47,
        "category": "Fiction",
        "title": "The Girl Who Collected Lost Buttons",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🔘 Every day on her walk to school, little Amba found a lost button on the ground — red, blue, wooden, shiny. She kept them all in a jar. 🫙\n\n"
            "Her friends thought it was strange. \"Why collect JUNK?\"\n\n"
            "One day, her teacher's coat was missing a button, and she was too shy to ask for help.\n\n"
            "\"I might have one that matches,\" Amba said, pulling out her jar. She found the perfect blue button and sewed it on herself.\n\n"
            "\"You saved my favorite coat,\" the teacher smiled. \"How did you know?\"\n\n"
            "\"I always noticed the small things nobody else picked up,\" Amba said proudly. Her \"junk\" jar had just become the most useful thing in the whole school. 🧵"
        ),
        "think": "🤔 *Think About It!*\nAmba's small hobby ended up helping someone in a big way. Is there something small you collect or notice that others think is unimportant?",
        "moral": "✨ *Today's Lesson:* Small, quiet habits can turn out to matter more than anyone expects."
    },
    {
        "id": 48,
        "category": "Fiction",
        "title": "The Dragon's Library Card",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🐉 A young dragon named Fen wanted to borrow a book from the village library, but the librarian gasped. \"Dragons burn books! I can't let you in!\"\n\n"
            "Fen's eyes filled with sadness. \"I would never hurt a book. I just want to read about far-away oceans.\"\n\n"
            "The librarian hesitated, then whispered, \"One chance. Prove me wrong.\"\n\n"
            "Fen read carefully, turning pages with the very tip of one claw, holding his breath so no smoke would escape. 📖\n\n"
            "Weeks passed. Fen returned every book in perfect condition, and even brought a few interesting shells he'd found on his own reading trips.\n\n"
            "\"I judged you before I knew you,\" the librarian admitted. \"I'm sorry, Fen.\"\n\n"
            "\"That's alright,\" Fen smiled. \"Now you know me.\" 🌊"
        ),
        "think": "🤔 *Think About It!*\nThe librarian was afraid of Fen because of what dragons usually do, not because of who Fen actually was. Has anyone ever judged you before really knowing you? How did you show them who you really are?",
        "moral": "✨ *Today's Lesson:* People deserve a chance to show who they really are, instead of being judged by assumptions."
    },
    {
        "id": 49,
        "category": "Fiction",
        "title": "The Kite That Wanted to Touch the Sun",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🪁 A bright yellow kite named Sunny dreamed of flying so high he could touch the actual sun. \"Higher! Higher!\" he begged the wind.\n\n"
            "The string held him back, tugging gently. \"Why won't you let me go?!\" Sunny complained to his string.\n\n"
            "One gusty day, the string finally snapped! Sunny soared free, higher than ever before — thrilling, at first.\n\n"
            "But soon the wind grew wild and tossed him around with no control. Sunny spun, torn, and finally crashed into a thorny bush, stuck and alone. 😢\n\n"
            "A boy found him days later, patched his torn paper, and tied on a new string.\n\n"
            "This time, when the string gently held him back, Sunny didn't complain. \"You're not holding me back,\" he realized. \"You're what lets me fly at all.\" 🧵☀️"
        ),
        "think": "🤔 *Think About It!*\nSunny thought the string was holding him back, but it was actually keeping him safe and steady. Are there rules or people in your life that feel limiting but actually help you?",
        "moral": "✨ *Today's Lesson:* What feels like a limit is sometimes exactly what allows us to soar safely."
    },
    {
        "id": 50,
        "category": "Fiction",
        "title": "The Mapmaker Who Drew Blank Spaces",
        "age": "Ages 5–7 🚀",
        "tradition": "Fiction 📖",
        "text": (
            "🗺️ Old Master Cato was the finest mapmaker in the kingdom, but everyone whispered about his strange habit — he always left one corner of every map blank.\n\n"
            "\"Why don't you fill it in?\" a young apprentice asked. \"You know every road, every river!\"\n\n"
            "Cato smiled. \"I leave space for what I haven't discovered yet. A map that thinks it knows everything stops explorers from looking further.\"\n\n"
            "The apprentice frowned, unsatisfied, and years later, filled in every last blank space on his own maps proudly.\n\n"
            "But travelers using his \"complete\" maps often got confused when new paths appeared that weren't drawn.\n\n"
            "Meanwhile, travelers using Cato's maps, with the honest blank corner, always kept their eyes open — and always found their way. 🧭"
        ),
        "think": "🤔 *Think About It!*\nCato believed leaving room for what he didn't know made his maps better, not worse. Is it okay to say \"I don't know yet\" about something? Why might that be helpful?",
        "moral": "✨ *Today's Lesson:* Admitting what we don't know keeps our minds open to learning more."
    },
    {
        "id": 51,
        "category": "Fiction",
        "title": "The Last Lighthouse Keeper on Mars",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "🚀 In the year 2150, Zoya was the only person living at Signal Station One, a tiny lighthouse-like beacon on Mars that guided spaceships safely to the colony. 🔴\n\n"
            "\"Doesn't it get lonely?\" her brother asked over the video call from Earth.\n\n"
            "\"Sometimes,\" Zoya admitted. \"But every ship that lands safely because of my light — that's a hundred lives I helped, even though I never meet them.\"\n\n"
            "One stormy Martian night, a dust storm knocked out half her equipment. Zoya worked for hours, freezing, repairing wires by hand, because a supply ship was due to land.\n\n"
            "When the ship finally landed safely, the pilot radioed: \"Thank you, Signal One. We saw your light through the whole storm.\"\n\n"
            "Zoya smiled alone in her small station, no crowd cheering, no medal waiting — just the quiet knowledge that her work had truly mattered. 🌌"
        ),
        "think": "🤔 *Think About It!*\nZoya did something important even though nobody was there to see it or thank her in person. Have you ever done a good job at something even when no one was watching?",
        "moral": "✨ *Today's Lesson:* The most meaningful work is often done quietly, without needing applause to make it worthwhile."
    },
    {
        "id": 52,
        "category": "Fiction",
        "title": "The Clockmaker's Extra Hour",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "⏰ An old clockmaker named Mr. Aldous built a peculiar clock that added one secret extra hour to every day — an hour that only he could enter, hidden between 11:59 and midnight.\n\n"
            "In that hidden hour, he wasn't tired from work or rushed by chores. He used it to write letters to his grandchildren, water his garden, and simply sit and think.\n\n"
            "One day his granddaughter found the strange clock. \"What's this extra hour for, Grandpa?\"\n\n"
            "\"It's not really extra,\" he chuckled. \"I just decided that one hour of my regular day belonged only to the things that mattered most to me — not errands, not rushing. Just... this.\"\n\n"
            "\"You didn't need a magic clock at all,\" she realized. \"You just needed to choose.\"\n\n"
            "\"Exactly,\" he smiled, handing her a small notebook. \"Now you choose your hour too.\" 📖✨"
        ),
        "think": "🤔 *Think About It!*\nMr. Aldous didn't actually get more hours — he just chose to protect one for what mattered most. If you had one guaranteed hour a day just for yourself, what would you spend it on?",
        "moral": "✨ *Today's Lesson:* We can't add time to our day, but we can choose to protect a little of it for what matters most."
    },
    {
        "id": 53,
        "category": "Fiction",
        "title": "The Girl Who Spoke to Rivers",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "🏞️ In a village by a wide river, a girl named Noor could hear the water whisper secrets — or so she believed. She'd sit by the bank for hours, listening. 💧\n\n"
            "\"You're wasting your time talking to water,\" her cousins teased.\n\n"
            "But Noor noticed things others missed: when the river ran low before a drought, when it rose too fast before a flood, when fish gathered strangely before a storm.\n\n"
            "One year, she warned the village elders, \"The river feels wrong. Move the boats to higher ground.\" They doubted her — but did it anyway, just in case.\n\n"
            "That night, a flash flood swept through. Every boat was safe.\n\n"
            "\"How did you know?\" the elders asked in wonder.\n\n"
            "\"I didn't hear magic words,\" Noor admitted. \"I just paid attention, every single day, longer than anyone else bothered to.\" 🌊"
        ),
        "think": "🤔 *Think About It!*\nNoor's \"magic\" was really just careful, patient attention over a long time. What is something you could learn a lot about if you paid close attention to it every day?",
        "moral": "✨ *Today's Lesson:* What looks like magic is often just patient, careful attention that others didn't take the time to give."
    },
    {
        "id": 54,
        "category": "Fiction",
        "title": "The Painter Who Ran Out of Blue",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "🎨 A young painter named Leo was famous for his stunning blue oceans — but one day, his last drop of blue paint ran dry, and no shop in his small town sold more.\n\n"
            "\"My art is ruined,\" Leo despaired, staring at his empty jar.\n\n"
            "His grandmother handed him charcoal, red clay dust, and yellow flower petals instead. \"Paint the ocean with what you have.\"\n\n"
            "Frustrated, Leo tried anyway — a grey, fiery, golden ocean, nothing like reality.\n\n"
            "When he showed it at the town fair, people stopped and stared, moved in a way his \"realistic\" blue oceans never quite achieved. \"It feels like a storm, and a sunset, and hope, all at once,\" one visitor whispered.\n\n"
            "Leo realized his limitation had pushed him toward something more honest than any blue paint ever had. 🌅"
        ),
        "think": "🤔 *Think About It!*\nLeo made something better BECAUSE he couldn't do things the usual way. Has running out of something, or not having what you needed, ever led you to a better idea?",
        "moral": "✨ *Today's Lesson:* Limitations can push us toward creativity we wouldn't have found any other way."
    },
    {
        "id": 55,
        "category": "Fiction",
        "title": "Nobody's Village",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "🏘️ Deep in a valley lived an invisible village — its people could turn unseen whenever they wished, and most chose to stay hidden all day, avoiding each other to skip the awkwardness of talking.\n\n"
            "A boy named Tomas grew tired of feeling alone despite living among hundreds of people. One morning, he chose to stay visible, all day, no matter how uncomfortable it felt.\n\n"
            "At first, people stared, confused. Slowly, one girl stayed visible too. Then an old man. Then a whole family.\n\n"
            "By evening, dozens of villagers stood together in the square, visible, awkward, laughing nervously — but together for the first time in years. 🌟\n\n"
            "\"We could always choose to be seen,\" Tomas realized. \"We just needed someone to go first.\" 💛"
        ),
        "think": "🤔 *Think About It!*\nTomas felt awkward being the first one to be seen, but it helped everyone else feel brave too. Have you ever had to go first at something uncomfortable so others could follow?",
        "moral": "✨ *Today's Lesson:* Connection often just needs someone brave enough to go first, even when it feels uncomfortable."
    },
    {
        "id": 56,
        "category": "Fiction",
        "title": "The Boy Who Traded His Shadow",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "👤 A mysterious trader offered young Kofi a deal: \"Give me your shadow, and I'll give you a bag of gold coins.\"\n\n"
            "Kofi, dazzled by the shiny coins, agreed instantly. His shadow slid away into the trader's bag, and Kofi walked home shadowless but rich.\n\n"
            "At first it was thrilling — new toys, new sweets. But soon, other children whispered, \"Why doesn't he have a shadow? Something is wrong with him.\" They avoided him at play. 😔\n\n"
            "Kofi realized his shadow, ordinary and unnoticed before, had made him feel normal, connected, like everyone else. The gold couldn't buy that feeling back.\n\n"
            "He found the trader again. \"Take back every coin. Just give me my shadow.\"\n\n"
            "The trader smiled knowingly and returned it. Kofi walked home poorer in coins, but whole again. 🌗"
        ),
        "think": "🤔 *Think About It!*\nKofi thought gold was worth more than his shadow, until he lost the shadow. Is there something ordinary about you — that you don't think much about — that actually matters more than you realize?",
        "moral": "✨ *Today's Lesson:* Some ordinary things we barely notice turn out to matter more than the shiniest rewards."
    },
    {
        "id": 57,
        "category": "Fiction",
        "title": "The Storyteller's Empty Chair",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "🪑 Every evening, the village storyteller Baba Rafiq told tales beside the fire, but he always left one chair completely empty beside him. Nobody knew why.\n\n"
            "A curious girl named Lila finally asked, \"Baba, why do you never let anyone sit there?\"\n\n"
            "\"That chair is for the next storyteller,\" he said. \"One day I will be gone, and someone must be ready to sit there and keep the stories alive. I leave it empty so everyone remembers it's waiting for someone.\"\n\n"
            "Lila thought about this for weeks. Slowly, she began remembering his stories, word for word, practicing them quietly to herself.\n\n"
            "One evening, when Baba Rafiq grew too tired to speak, Lila walked to the empty chair and sat down. \"May I try?\" she asked.\n\n"
            "Baba Rafiq smiled through tired eyes. \"The chair was always waiting for you.\" 🔥📖"
        ),
        "think": "🤔 *Think About It!*\nBaba Rafiq kept a chair empty for years, trusting someone would eventually be ready to fill it. Is there something important — a skill, a tradition, a responsibility — that you might be preparing to carry forward one day?",
        "moral": "✨ *Today's Lesson:* Important things are passed down when someone is patient enough to wait, and someone else is ready to step forward."
    },
    {
        "id": 58,
        "category": "Fiction",
        "title": "The Kingdom That Forgot to Say Thank You",
        "age": "Ages 8–10 📚",
        "tradition": "Fiction 📖",
        "text": (
            "👑 In the kingdom of Velora, people were polite but had quietly stopped saying \"thank you\" — it seemed old-fashioned, unnecessary between busy people.\n\n"
            "The farmers stopped feeling appreciated and grew less food. The blacksmiths stopped feeling valued and made weaker tools. Slowly, without anyone noticing exactly why, the whole kingdom grew a little colder, a little more tired. ❄️\n\n"
            "A young servant girl named Priya still whispered \"thank you\" to everyone — the baker, the guard, the queen's tired horse. People thought she was strange.\n\n"
            "But those she thanked started working a little harder, smiling a little more, trying a little longer — just from being noticed.\n\n"
            "Slowly, others copied her. \"Thank you\" spread through Velora like warm sunlight after a long winter.\n\n"
            "The kingdom never realized how much two small words had been worth, until they'd almost lost them completely. ☀️"
        ),
        "think": "🤔 *Think About It!*\nSaying \"thank you\" seemed small, but it changed how the whole kingdom felt. Who is someone you could say a genuine thank you to today?",
        "moral": "✨ *Today's Lesson:* Small words of gratitude can quietly change how an entire community feels."
    },
    {
        "id": 59,
        "category": "Drama",
        "title": "The Day Mama Forgot My Name",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "😟 Little Tia tugged Mama's sleeve at the busy market. \"Mama! Mama!\" But Mama, juggling bags and a phone call, said, \"Not now, sweetie,\" without even looking down.\n\n"
            "Tia's lip wobbled. \"Did Mama forget me?\" she worried, feeling very small in the crowd.\n\n"
            "When they got home, Mama finally knelt down, put everything away, and looked right into Tia's eyes. \"I'm sorry I was busy, my love. Tell me everything now.\" 💕\n\n"
            "Tia told her all about the butterfly she'd seen, talking and talking. Mama listened to every word.\n\n"
            "\"You didn't forget me,\" Tia realized happily. \"You were just busy for a little while.\" 🦋"
        ),
        "think": "🤔 *Think About It!*\nHave you ever felt like someone forgot about you when they were just busy for a moment? How did it feel when they came back to listen?",
        "moral": "✨ *Today's Lesson:* Being busy for a moment doesn't mean someone stopped caring — love comes back around."
    },
    {
        "id": 60,
        "category": "Drama",
        "title": "New Shoes, New Steps",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "👟 It was little Arjun's very first day of preschool, and his new shoes felt stiff and strange. \"I don't want to go,\" he whispered, holding tight to Papa's hand at the gate.\n\n"
            "Inside, so many new faces, new sounds, new everything. Arjun's tummy felt fluttery. 😰\n\n"
            "A girl named Ria sat beside him with a box of crayons. \"Want to draw with me?\" she asked with a big smile.\n\n"
            "Slowly, Arjun picked up a red crayon. They drew together, quiet at first, then giggling by snack time.\n\n"
            "When Papa came to pick him up, Arjun ran to him excitedly. \"I made a friend! Can I wear my new shoes again tomorrow?\" 😊👟"
        ),
        "think": "🤔 *Think About It!*\nHave you ever felt nervous about something new, like a first day somewhere? What helped you feel better?",
        "moral": "✨ *Today's Lesson:* New things feel scary at first, but they often become wonderful once we give them a chance."
    },
    {
        "id": 61,
        "category": "Drama",
        "title": "The Blanket That Went to the Wash",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "🧸 Little Sam had one soft, fuzzy blanket named Cloudy that he carried absolutely everywhere. One day, Mama said, \"Cloudy is due for a wash — he's getting a little smelly!\"\n\n"
            "Sam's eyes went wide with worry. \"But what if he doesn't come back the same?!\" he cried.\n\n"
            "Mama gently placed Cloudy in the machine. Sam watched through the little window, sniffling, as Cloudy spun round and round. 🌀\n\n"
            "When the machine finally stopped, Mama pulled out Cloudy — warm, fluffy, and smelling like sunshine. 🌞\n\n"
            "Sam hugged him tight. \"You're even softer now!\" he laughed with relief.\n\n"
            "\"Some changes,\" Mama smiled, \"make things even better than before.\" 💙"
        ),
        "think": "🤔 *Think About It!*\nHave you ever worried about a change, like washing your favorite toy or trying new food, and then found out it was actually fine?",
        "moral": "✨ *Today's Lesson:* Some changes feel scary beforehand but turn out just fine, or even better, afterward."
    },
    {
        "id": 62,
        "category": "Drama",
        "title": "My Brother Got All the Cake",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "🎂 At the birthday party, little Naina watched her big brother get the piece of cake with the biggest pink flower on top. \"That's not fair! I wanted that piece!\" she pouted.\n\n"
            "She crossed her arms and refused to eat her own piece, even though it had chocolate sprinkles she usually loved.\n\n"
            "Her brother noticed her sad face. He looked at his flower piece, then at her. \"Here,\" he said, breaking off half the flower with his spoon and putting it on her plate. \"Sharing makes cake taste better anyway.\" 🍰\n\n"
            "Naina's frown turned into a big smile. \"Thank you!\" She took a huge, happy bite. 😋"
        ),
        "think": "🤔 *Think About It!*\nHave you ever felt upset about something small not being fair? What happened when someone decided to share?",
        "moral": "✨ *Today's Lesson:* Sharing turns a small disappointment into a moment of kindness for everyone."
    },
    {
        "id": 63,
        "category": "Drama",
        "title": "Grandpa's Chair Is Empty Today",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "🪑 Little Ana noticed Grandpa's favorite chair by the window was empty. \"Where's Grandpa?\" she asked Mama.\n\n"
            "\"Grandpa is resting at the hospital for a little while, so the doctors can help him feel strong again,\" Mama said softly.\n\n"
            "Ana felt a funny lump in her throat. She sat in Grandpa's chair and hugged his old, worn cushion. 💺\n\n"
            "\"Can I draw him a picture?\" she asked.\n\n"
            "She drew the sun, their garden, and Grandpa's favorite dog, and Mama helped mail it that very day.\n\n"
            "A week later, Grandpa came home, tired but smiling, and taped Ana's drawing right beside his chair. \"This made me feel better every single day,\" he said, hugging her tight. 💛"
        ),
        "think": "🤔 *Think About It!*\nHas someone you love ever been away or unwell? What is something small you could do to show them you're thinking of them?",
        "moral": "✨ *Today's Lesson:* Small gestures of love can reach someone even when we can't be right beside them."
    },
    {
        "id": 64,
        "category": "Drama",
        "title": "The Puzzle Piece That Didn't Fit",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "🧩 During playtime, little Ravi tried to jam a puzzle piece into the wrong spot, pushing and pushing. \"Go in!\" he grumbled, frustrated.\n\n"
            "His friend Meera watched. \"Maybe it belongs somewhere else,\" she said gently.\n\n"
            "Ravi huffed but tried the piece in a different spot — and click! It fit perfectly, completing the picture of a smiling sun. ☀️\n\n"
            "\"It just needed the right place,\" Ravi said, surprised.\n\n"
            "Meera smiled. \"Sometimes things — and people — just need to find where they truly belong.\" 🧩💛"
        ),
        "think": "🤔 *Think About It!*\nHave you ever tried to force something to work when it just needed a different approach? What happened when you tried something new?",
        "moral": "✨ *Today's Lesson:* If something doesn't fit right away, it might just belong somewhere else — that's okay."
    },
    {
        "id": 65,
        "category": "Drama",
        "title": "Why Is Papa Sad Today?",
        "age": "Ages 2–4 🧸",
        "tradition": "Drama 🎭",
        "text": (
            "😔 Little Kabir noticed Papa sitting very quietly on the sofa, not smiling like usual. \"Papa, why are you sad?\" he asked, climbing onto his lap.\n\n"
            "\"I had a hard day at work, beta,\" Papa said softly. \"Grown-ups feel sad sometimes too.\"\n\n"
            "Kabir thought hard, then ran to get his favorite toy elephant. \"Here, Papa. Elephant makes ME feel better.\" He placed it gently in Papa's hands. 🐘\n\n"
            "Papa smiled, really smiled, for the first time all day, and pulled Kabir into a warm hug. \"Thank you, beta. You made my day better already.\" 🤗"
        ),
        "think": "🤔 *Think About It!*\nHave you ever noticed someone you love feeling sad? What is a small, kind thing you could do to help them feel better?",
        "moral": "✨ *Today's Lesson:* Grown-ups have feelings too, and a small act of kindness can help anyone, big or small."
    },
    {
        "id": 66,
        "category": "Drama",
        "title": "The New Kid With the Funny Lunch",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "🍱 A new boy named Hiro joined class, and at lunchtime, some kids pointed and giggled at his food. \"Ew, what IS that? It smells weird!\" one boy said loudly.\n\n"
            "Hiro's face turned red, and he quietly closed his lunchbox, not eating another bite.\n\n"
            "Little Meera noticed and walked over. \"What is it? It actually smells really good,\" she said honestly, sitting beside him.\n\n"
            "\"It's onigiri — rice balls my grandma makes,\" Hiro said quietly. \"Want to try one?\"\n\n"
            "Meera took a bite. \"This is amazing! Can I bring you something from MY lunch tomorrow?\"\n\n"
            "The next day, they traded snacks and swapped stories about their families, and Hiro didn't feel like the \"weird new kid\" anymore — he felt like Meera's friend. 🍙💕"
        ),
        "think": "🤔 *Think About It!*\nHave you ever laughed at something just because it seemed different or unfamiliar? How do you think it felt for the other person?",
        "moral": "✨ *Today's Lesson:* Curiosity and kindness turn 'different' into 'interesting' — and can turn a stranger into a friend."
    },
    {
        "id": 67,
        "category": "Drama",
        "title": "Losing by One Point",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "🏀 In the final seconds of the school basketball game, little Dev missed the last shot. His team lost by just one point. 😞\n\n"
            "He sat alone on the bench, staring at the floor, feeling like he'd let everyone down.\n\n"
            "His coach sat beside him. \"You know what I saw out there? A boy who took the brave shot, even though it was scary, instead of passing it away out of fear.\"\n\n"
            "\"But we still lost,\" Dev mumbled.\n\n"
            "\"Yes,\" said Coach, \"but you'll take that shot again next time, and the next, until one day it goes in. That takes courage, not talent.\"\n\n"
            "Dev looked up, still sad, but a little less heavy. \"I'll practice all week,\" he said quietly. 🏀💪"
        ),
        "think": "🤔 *Think About It!*\nHave you ever lost at something you really wanted to win? What helped you feel okay about trying again?",
        "moral": "✨ *Today's Lesson:* Losing doesn't erase the courage it took to try — and trying again is how we get better."
    },
    {
        "id": 68,
        "category": "Drama",
        "title": "The Secret I Didn't Tell",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "🤫 Little Simran accidentally broke her mother's favorite vase while playing indoors, but quickly hid the pieces and said nothing. 💔\n\n"
            "For days, a heavy feeling sat in her tummy every time she saw the empty shelf where the vase used to sit.\n\n"
            "One evening, she couldn't hold it in anymore. \"Mama, I broke your vase. I was scared to tell you.\" Tears filled her eyes.\n\n"
            "Mama hugged her tightly. \"Thank you for telling me the truth, even though it was hard. That matters much more to me than any vase.\" 🏺💕\n\n"
            "Simran felt the heavy feeling in her tummy melt away completely, replaced by something light and warm. \"I feel so much better now,\" she whispered."
        ),
        "think": "🤔 *Think About It!*\nHave you ever kept a secret that made your tummy feel heavy? What happened when you finally told the truth?",
        "moral": "✨ *Today's Lesson:* Telling the truth feels scary at first, but it lifts a weight off your heart."
    },
    {
        "id": 69,
        "category": "Drama",
        "title": "Moving Day",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "📦 Boxes filled every room as little Farah watched her whole house get packed up. \"I don't want to move to a new city,\" she said, hugging her stuffed rabbit tightly. \"What if nobody likes me there?\"\n\n"
            "Papa sat beside the last box. \"I felt scared too, when I moved here as a boy. But you know what helped? I brought pieces of my old home with me — photos, favorite books, even this same old rabbit toy of mine that I gave to you.\" 🐰\n\n"
            "Farah looked down at her rabbit, surprised. \"This was YOURS?\"\n\n"
            "\"Yes, and it made new places feel a little like home. You'll make new friends, but you don't have to leave everything behind to do it.\" 💛\n\n"
            "Farah packed the rabbit carefully into her own special bag."
        ),
        "think": "🤔 *Think About It!*\nHave you ever had to leave somewhere familiar for somewhere new? What helped that new place start to feel like home?",
        "moral": "✨ *Today's Lesson:* We can carry pieces of what we love with us into new beginnings, so nothing is ever fully left behind."
    },
    {
        "id": 70,
        "category": "Drama",
        "title": "The Friend Who Moved Away",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "✈️ Little Aditi's best friend Wren was moving to a faraway city. On the last day of school together, they sat quietly at recess, not knowing what to say. 😢\n\n"
            "\"Will we still be best friends?\" Aditi asked, her voice shaking.\n\n"
            "\"We can write letters,\" Wren said. \"And Mom said we can video call sometimes.\"\n\n"
            "They made a promise: every full moon, no matter how far apart, they'd both look up at the same moon at the same time and think of each other. 🌕\n\n"
            "Months later, on a lonely night, Aditi looked up and saw the full moon glowing bright. She smiled, knowing Wren was probably looking at the exact same moon, right then, thinking of her too."
        ),
        "think": "🤔 *Think About It!*\nHave you ever had a friend move away? What is a way you could still feel close to them, even from far apart?",
        "moral": "✨ *Today's Lesson:* Distance changes how often we see someone, but it doesn't have to change how much we care."
    },
    {
        "id": 71,
        "category": "Drama",
        "title": "Two Left Shoes on Picture Day",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "📸 On school picture day, little Omar rushed out the door and didn't notice until he sat down in class — he was wearing two different left shoes! 😱\n\n"
            "\"Everyone's going to laugh at me,\" he panicked, hiding his feet under the desk all morning.\n\n"
            "When picture time came, a classmate named Zoe noticed and whispered, \"Everyone has something a little weird about them today. Look — my hair ribbon is crooked, and Sam has a marker stain on his shirt.\"\n\n"
            "Omar looked around and realized she was right — nobody was perfectly put together.\n\n"
            "He walked up for his photo, smiled a real, big smile, and didn't hide his feet at all.\n\n"
            "When the pictures came back, his smile was the best part of the photo — nobody even noticed the shoes. 😄"
        ),
        "think": "🤔 *Think About It!*\nHave you ever worried everyone would notice a small mistake you made? Did anyone actually notice as much as you thought?",
        "moral": "✨ *Today's Lesson:* Small mistakes feel huge to us, but they rarely matter as much to everyone else."
    },
    {
        "id": 72,
        "category": "Drama",
        "title": "The Fight Over the Last Swing",
        "age": "Ages 5–7 🚀",
        "tradition": "Drama 🎭",
        "text": (
            "🛝 At recess, little Yusuf and his friend Priya both ran for the last empty swing at the exact same time. \"I got here first!\" Yusuf shouted. \"No, I did!\" Priya argued back.\n\n"
            "They both grabbed the swing, tugging, until the teacher walked over. \"Instead of pulling it apart, why don't you figure out how to share it?\"\n\n"
            "Yusuf and Priya looked at each other, annoyed at first. Then Priya said, \"Ten swings each, then we switch?\"\n\n"
            "Yusuf nodded slowly. \"Okay. You go first.\"\n\n"
            "By the time recess ended, they'd taken turns four times, laughing and counting swings together, forgetting they'd ever been arguing at all. 😄"
        ),
        "think": "🤔 *Think About It!*\nHave you ever argued with a friend over something small? What helped you find a way to share instead of fight?",
        "moral": "✨ *Today's Lesson:* Most fights over 'who's right' can be solved by finding a way to share instead."
    },
    {
        "id": 73,
        "category": "Drama",
        "title": "The Report Card I Hid Under My Bed",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "📋 Ishaan stared at his report card — lower marks than he'd ever gotten before. Scared of disappointing his parents, he shoved it under his mattress and said nothing for three whole days. 😰\n\n"
            "But the secret grew heavier each night, keeping him awake, making him snap at his little sister over nothing.\n\n"
            "Finally, he pulled it out and handed it to his mother, hands trembling. \"I'm sorry. I did badly and I was scared to show you.\"\n\n"
            "His mother looked at it quietly, then at him. \"I'm not happy about the marks. But I'm much more worried that you were scared to tell me anything. Marks can improve. Trust between us matters more.\" 💛\n\n"
            "They sat together that evening making a study plan, and for the first time in days, Ishaan slept peacefully."
        ),
        "think": "🤔 *Think About It!*\nHave you ever hidden something because you were scared of someone's reaction? What made it hard, or easier, to finally share it?",
        "moral": "✨ *Today's Lesson:* Hiding a mistake makes it heavier — sharing it, even when scary, is how we start fixing it."
    },
    {
        "id": 74,
        "category": "Drama",
        "title": "When Dad Lost His Job",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "💼 One evening, ten-year-old Maya overheard her parents talking quietly in the kitchen. \"The company let me go,\" Dad said, his voice tired. \"We'll need to be careful with money for a while.\"\n\n"
            "Maya felt scared — would they have to move? Would things change forever?\n\n"
            "The next weeks were different — fewer outings, simpler meals — but Maya noticed something else too: Dad started picking her up from school every day, and they'd talk the whole walk home. 🚶‍♂️\n\n"
            "\"I miss the old ice cream trips,\" Maya admitted one day.\n\n"
            "\"Me too,\" Dad said, \"but I don't miss rushing past you every evening. I found a new job last week — but I'm going to keep walking you home anyway.\" 🍦\n\n"
            "Maya realized hard times had brought them something unexpected — more time together."
        ),
        "think": "🤔 *Think About It!*\nHave you ever gone through a hard change at home? Was there anything unexpected — even small — that turned out okay, or good, during that time?",
        "moral": "✨ *Today's Lesson:* Hard times are still hard, but they can also reveal what truly matters most."
    },
    {
        "id": 75,
        "category": "Drama",
        "title": "The Team That Didn't Pick Me",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "⚽ During gym class, team captains picked players one by one — and little Tariq was picked last, again. He walked to his spot on the field with his head down, cheeks burning. 😔\n\n"
            "After class, his friend Noah caught up with him. \"That felt unfair. You're actually really fast.\"\n\n"
            "\"Then why am I always picked last?\" Tariq asked bitterly.\n\n"
            "\"Because you don't shoot the ball much, so nobody's seen what you can do,\" Noah said honestly. \"Maybe show them next time instead of hanging back.\"\n\n"
            "The next game, Tariq ran hard and finally took a shot — and scored! His teammates cheered, surprised.\n\n"
            "He wasn't picked first the very next week either, but he was picked earlier. \"Change takes more than one game,\" he told himself, \"but it's starting.\" ⚽✨"
        ),
        "think": "🤔 *Think About It!*\nHave you ever felt overlooked or picked last for something? What is one small step you could take to show others what you're capable of?",
        "moral": "✨ *Today's Lesson:* Being overlooked doesn't mean staying overlooked — showing up and trying can slowly change things."
    },
    {
        "id": 76,
        "category": "Drama",
        "title": "My Best Friend's New Best Friend",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "👭 Little Sana watched her best friend Ria laughing with a new girl at lunch, sitting in Sana's usual spot. A tight, jealous feeling squeezed her chest. 😞\n\n"
            "For days, Sana felt pushed aside, but instead of saying anything, she just grew quieter and quieter around Ria.\n\n"
            "Finally, Ria noticed. \"Are you upset with me?\"\n\n"
            "\"You have a new best friend now,\" Sana blurted out, tears stinging.\n\n"
            "Ria looked surprised. \"Priya is nice, but she's not replacing you. I didn't realize you felt left out — I should have invited you to sit with us.\"\n\n"
            "The next day, all three girls sat together, and slowly, Sana realized having more friends didn't mean having less of Ria. 💕"
        ),
        "think": "🤔 *Think About It!*\nHave you ever felt jealous when a friend made another friend? What helped, or might help, you feel less worried about it?",
        "moral": "✨ *Today's Lesson:* Friendship isn't a limited pie — someone having another friend doesn't mean less love for you."
    },
    {
        "id": 77,
        "category": "Drama",
        "title": "The Night the Power Went Out",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "🕯️ A huge storm knocked out the power across the whole neighborhood. No lights, no TV, no phone charging — nine-year-old Leo groaned, \"This is the WORST night ever.\"\n\n"
            "His mother lit candles and pulled out an old deck of cards. \"Let's make the best of it.\"\n\n"
            "By candlelight, the whole family played cards, told silly ghost stories, and Dad even brought out his old guitar, badly out of tune, singing songs from his own childhood. 🎸\n\n"
            "Leo laughed harder that night than he had in weeks.\n\n"
            "When the lights finally flickered back on near midnight, nobody rushed to turn on their screens right away. They just sat together a little longer, oddly reluctant for the ordinary night to end. ✨"
        ),
        "think": "🤔 *Think About It!*\nHave you ever had an unexpected inconvenience turn into a surprisingly fun memory? What made it special?",
        "moral": "✨ *Today's Lesson:* Sometimes losing what we're used to reveals a simpler kind of togetherness we'd forgotten."
    },
    {
        "id": 78,
        "category": "Drama",
        "title": "Grandma Forgets My Name Now",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "👵 On their weekly visit, Grandma looked at ten-year-old Divya and asked, \"Now, whose lovely daughter are you?\" Divya's stomach dropped. \"Grandma, it's me — Divya!\"\n\n"
            "Grandma smiled kindly but confused. Mom pulled Divya aside gently. \"Grandma's memory is changing as she gets older. It's called dementia. It's not that she doesn't love you — her mind just has trouble holding onto things now.\"\n\n"
            "Divya felt sad and a little scared. The next visit, instead of expecting Grandma to remember, she brought old photo albums and pointed to pictures. \"This is us at the beach, Grandma. Remember the shells we collected?\"\n\n"
            "Grandma's eyes lit up. \"Oh, yes! Such a happy day.\" She might not remember Divya's name every time, but together, they still made new happy moments. 💛"
        ),
        "think": "🤔 *Think About It!*\nHas someone you loved changed in a way that was hard to understand? What helped you feel connected to them anyway?",
        "moral": "✨ *Today's Lesson:* Love can find new ways to connect, even when memory or circumstances change."
    },
    {
        "id": 79,
        "category": "Drama",
        "title": "The Apology I Almost Didn't Give",
        "age": "Ages 8–10 📚",
        "tradition": "Drama 🎭",
        "text": (
            "😤 During a group project, ten-year-old Karan snapped angrily at his partner Wei, blaming him for a mistake that was actually Karan's own fault. Wei looked hurt and stayed quiet the rest of class.\n\n"
            "Karan knew he should apologize, but his pride kept whispering, \"Just let it go, it's not a big deal.\"\n\n"
            "That night, Karan couldn't stop thinking about Wei's hurt expression. The next morning, hands sweaty, he walked up to Wei before class. \"I was wrong yesterday. It was my mistake, not yours, and I shouldn't have snapped at you. I'm sorry.\"\n\n"
            "Wei's face relaxed into a small smile. \"Thanks for saying that. It actually means a lot.\"\n\n"
            "Karan felt lighter than he had all night — that one hard sentence had been worth more than his pride. 🤝"
        ),
        "think": "🤔 *Think About It!*\nHas your pride ever made it hard to say sorry, even when you knew you should? What finally helped you say it?",
        "moral": "✨ *Today's Lesson:* Swallowing pride to give an honest apology is hard, but it almost always feels better than staying silent."
    },
    {
        "id": 80,
        "category": "Fun",
        "title": "The Burping Contest Bandicoot",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🐹 Bindi the bandicoot could burp louder than anyone in the whole forest. BUUURRRP! 😂\n\n"
            "\"That's disgusting,\" said the prim rabbit, wrinkling her nose.\n\n"
            "But when the forest held its Silly Sounds Festival, Bindi's thunderous burp won FIRST PRIZE, echoing across the whole valley! 🏆\n\n"
            "Even the rabbit couldn't stop giggling. \"Okay, that WAS impressive,\" she admitted, snorting with laughter.\n\n"
            "Bindi grinned proudly. \"Being a LITTLE bit silly is basically my superpower!\" she cheered, letting out one more enormous BUUURRRP for good measure. 🎉"
        ),
        "think": "🤔 *Think About It!*\nWhat's the silliest sound YOU can make? Can you try it right now and see who laughs?",
        "moral": "✨ *Today's Lesson:* Being a little silly sometimes is just as wonderful as being serious."
    },
    {
        "id": 81,
        "category": "Fun",
        "title": "Grandpa's Dancing Slippers",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🩰 Grandpa's old fuzzy slippers had a secret — whoever wore them couldn't stop dancing! 💃\n\n"
            "Little Priya slipped them on to fetch her ball, and suddenly — wiggle wiggle, twirl twirl! She couldn't stop no matter how hard she tried, giggling the whole time. 😂\n\n"
            "Mama walked in and slipped on the OTHER slipper by accident. Now they were BOTH dancing around the living room, bumping into the sofa, laughing so hard they could barely breathe. 🛋️\n\n"
            "Even the family dog started spinning in silly circles, barking along.\n\n"
            "When they finally kicked off the slippers, breathless, Priya giggled, \"Best. Chore. Ever.\" 🐕✨"
        ),
        "think": "🤔 *Think About It!*\nIf your shoes made you dance every time you wore them, what silly place would you want to dance in?",
        "moral": "✨ *Today's Lesson:* A little unexpected silliness can turn an ordinary moment into a happy memory."
    },
    {
        "id": 82,
        "category": "Fun",
        "title": "The Day My Dog Wore My Pants",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🐶 Little Zoya left her pants on the floor while getting ready, and her puppy Biscuit decided they looked VERY comfortable. 😆\n\n"
            "Somehow, Biscuit wiggled his back legs right into them and trotted around the house wearing Zoya's pants like the fanciest dog in town! 👖\n\n"
            "\"Biscuit! Those are MY pants!\" Zoya laughed so hard she fell onto the couch.\n\n"
            "Biscuit paraded proudly through the living room, tripping over the extra-long legs, tail wagging with pride the whole time.\n\n"
            "Mama snapped a photo before gently helping Biscuit out of the tangle. \"Best dressed dog in the whole neighborhood,\" she declared, still giggling. 📸"
        ),
        "think": "🤔 *Think About It!*\nHas your pet, or a stuffed animal, ever done something silly that made you laugh out loud?",
        "moral": "✨ *Today's Lesson:* The silliest, most unplanned moments often become our favorite memories to laugh about later."
    },
    {
        "id": 83,
        "category": "Fun",
        "title": "Soup Made of Giggles",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🍲 Chef Pablo the penguin claimed he had invented the world's silliest recipe: Giggle Soup. \"One cup of jokes, two tickles, and a splash of funny faces!\" he announced. 🐧\n\n"
            "He stirred the pretend pot dramatically, then made the silliest face imaginable at his customers — tongue out, eyes crossed! 🤪\n\n"
            "Everyone at the table burst out laughing — HA HA HA!\n\n"
            "\"See?\" Pablo grinned. \"Giggle Soup works every time!\"\n\n"
            "He served invisible bowls to everyone, and the whole restaurant kept right on giggling, long after the imaginary soup was finished. 😂🥄"
        ),
        "think": "🤔 *Think About It!*\nIf YOU made a silly soup out of things that make you laugh, what ingredients would you put in it?",
        "moral": "✨ *Today's Lesson:* Laughter is contagious — sharing it is one of the easiest gifts to give."
    },
    {
        "id": 84,
        "category": "Fun",
        "title": "The Sneezing Elephant Parade",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🐘 Ellie the elephant had the ITCHIEST nose from all the dusty flowers in the jungle. \"Ah... ah... AHCHOOO!\" 🌼\n\n"
            "Her sneeze was SO powerful it blew all the leaves off three trees and knocked a monkey clean off his branch! 🙉\n\n"
            "\"Bless you!\" shouted every animal at once, then burst into giggles at the huge mess of leaves everywhere.\n\n"
            "Ellie sneezed again — ACHOO! — and this time blew a whole line of ducks straight into the river, quacking indignantly. 🦆\n\n"
            "By the end of the day, the whole jungle had joined a silly parade, marching behind Ellie and her mighty, mighty sneezes. 🎉"
        ),
        "think": "🤔 *Think About It!*\nWhat is the biggest sneeze YOU have ever done? Did anyone laugh?",
        "moral": "✨ *Today's Lesson:* Even the messiest accidents can turn into the funniest shared moments."
    },
    {
        "id": 85,
        "category": "Fun",
        "title": "My Pet Rock Runs Away",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "🪨 Little Theo loved his pet rock, Pebbles, and carried him everywhere in a little box. One windy day at the park, a huge gust — WHOOSH! — knocked Pebbles right out of the box and rolling down the hill! 💨\n\n"
            "\"Pebbles is running away!\" Theo shouted dramatically, chasing after him, giggling the whole time.\n\n"
            "Pebbles rolled under a bench, bounced off a bush, and finally stopped near a duck pond, looking (as always) exactly the same.\n\n"
            "Theo scooped him up triumphantly. \"You had quite the adventure today, Pebbles!\"\n\n"
            "That night, he told his whole family the epic tale of Pebbles' Great Escape, adding more excitement with every retelling. 😄🪨"
        ),
        "think": "🤔 *Think About It!*\nDo you have a favorite toy that goes on 'adventures' with you? What silly story could you make up about it?",
        "moral": "✨ *Today's Lesson:* Imagination can turn even a rock into the hero of the silliest, most fun stories."
    },
    {
        "id": 86,
        "category": "Fun",
        "title": "The Upside-Down Umbrella Day",
        "age": "Ages 2–4 🧸",
        "tradition": "Fun 🎈",
        "text": (
            "☂️ On a windy, rainy day, little Maya's umbrella suddenly flipped completely inside out — WHOOSH! 💨\n\n"
            "\"It looks like a funny flower now!\" she laughed, holding it up proudly.\n\n"
            "Instead of fixing it right away, she skipped through puddles holding her funny flower-umbrella, rain splashing everywhere. 💦\n\n"
            "Her big brother saw her and flipped HIS umbrella inside out too, and soon a whole group of kids were splashing around with their silly flower umbrellas held high. 🌸\n\n"
            "\"Best rainy day EVER,\" Maya giggled, twirling in the puddles."
        ),
        "think": "🤔 *Think About It!*\nHas something ever gone 'wrong' — like your umbrella flipping — that turned into something fun instead?",
        "moral": "✨ *Today's Lesson:* When plans go a little sideways, sometimes that's exactly when the fun begins."
    },
    {
        "id": 87,
        "category": "Fun",
        "title": "The Homework That Ate Itself",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "📝 Little Jenny left her math homework on the kitchen table, right next to a plate of chocolate cake. When she came back — her worksheet had chocolate handprints ALL over it! 🍫\n\n"
            "\"My baby brother ATE my homework!\" she gasped, staring at little Ravi, chocolate smeared cheek to cheek, grinning innocently.\n\n"
            "She tried to explain to her teacher the next day. \"My homework got... eaten. Sort of.\"\n\n"
            "Her teacher raised an eyebrow, unconvinced, until Jenny showed a photo of Ravi's chocolatey masterpiece.\n\n"
            "The whole class burst out laughing, and her teacher, still chuckling, gave her one extra day. \"Best excuse I've heard all year,\" she admitted. 😂🍰"
        ),
        "think": "🤔 *Think About It!*\nWhat's the funniest excuse or mix-up that's ever happened with your homework or chores?",
        "moral": "✨ *Today's Lesson:* Even the most annoying accidents can turn into the best stories to tell later."
    },
    {
        "id": 88,
        "category": "Fun",
        "title": "Pajama Day at School",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🛌 Half-asleep, little Arun rushed to catch the school bus — and didn't realize until he sat down in class that he'd forgotten to change out of his dinosaur pajamas! 🦖\n\n"
            "\"Arun, why are you in your PJs?\" his friend whispered, giggling.\n\n"
            "Arun looked down, horrified — then noticed his teacher's kind smile. \"Well,\" she announced to the class, \"today is officially Pajama Day, everyone! Arun gets to pick tomorrow's fun theme too!\"\n\n"
            "The whole class cheered. By lunchtime, three other kids had \"accidentally\" worn their pajamas too, giggling in solidarity. 😄\n\n"
            "Arun, once mortified, walked home that day feeling like the most popular kid in school."
        ),
        "think": "🤔 *Think About It!*\nHas an embarrassing mistake ever turned into something everyone ended up enjoying together?",
        "moral": "✨ *Today's Lesson:* An embarrassing moment can turn into a fun memory if you let yourself laugh along with everyone else."
    },
    {
        "id": 89,
        "category": "Fun",
        "title": "The Great Broccoli Rebellion",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🥦 At dinner, little Zara declared, \"Broccoli should NOT be allowed at this table!\" and staged a dramatic protest, holding up a sign made of napkins: \"NO MORE TREES ON MY PLATE!\" 🪧\n\n"
            "Her little brother joined the protest, marching around the kitchen chanting, \"No more trees! No more trees!\"\n\n"
            "Dad, trying not to laugh, negotiated: \"What if the broccoli trees get a cheese blanket?\" He sprinkled melted cheese on top. 🧀\n\n"
            "Zara eyed it suspiciously, took one tiny bite... then another. \"Okay,\" she admitted, \"cheese-blanket broccoli trees are ALLOWED at this table.\"\n\n"
            "The Great Broccoli Rebellion ended peacefully, with full bellies and a lot of giggles. 😄"
        ),
        "think": "🤔 *Think About It!*\nIs there a food you don't love that might taste better with a silly new name or a fun twist?",
        "moral": "✨ *Today's Lesson:* A little creativity and humor can turn a stubborn 'no' into a happy 'yes.'"
    },
    {
        "id": 90,
        "category": "Fun",
        "title": "Mr. Wobble's Wonky Bicycle",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🚲 Old Mr. Wobble's bicycle had one wheel slightly smaller than the other, so he wobbled up and DOWN the whole street every single ride. 😆\n\n"
            "Kids would gather just to watch him pass — bob, bob, bob — waving cheerfully with every up-and-down bump.\n\n"
            "\"Why don't you fix it, Mr. Wobble?\" a boy named Tomi asked one day.\n\n"
            "Mr. Wobble laughed heartily. \"And lose my famous wobble? This bike has made more kids smile than a perfectly straight one ever could!\"\n\n"
            "He wobbled off down the road, whistling, waving at every giggling child along the way, proud of his silly, imperfect ride. 🎶"
        ),
        "think": "🤔 *Think About It!*\nIs there something a little imperfect about you or your things that actually makes people smile or makes you unique?",
        "moral": "✨ *Today's Lesson:* Things that aren't perfect can still bring more joy than perfect ones do."
    },
    {
        "id": 91,
        "category": "Fun",
        "title": "The Burp That Traveled the World",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🌍 During a video call with cousins in three different countries, little Aarav let out the LOUDEST burp anyone had ever heard. \"BURRRRP!\" 😂\n\n"
            "The screen froze for a second, then all three cousins burst out laughing at exactly the same moment, their laughter echoing across time zones.\n\n"
            "\"That burp just traveled around the ENTIRE world in one second!\" his cousin in London giggled.\n\n"
            "For weeks after, the family group chat was filled with burp emoji jokes and remember-when messages. 📱😂\n\n"
            "Aarav became legendary in his family for \"The Burp Heard Round the World,\" and he couldn't have been prouder."
        ),
        "think": "🤔 *Think About It!*\nWhat's a funny family moment that everyone still laughs about and retells, even much later?",
        "moral": "✨ *Today's Lesson:* Silly shared moments become the inside jokes that bring families closer, even across long distances."
    },
    {
        "id": 92,
        "category": "Fun",
        "title": "My Little Sister the Superhero",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🦸 Little Rhea tied a bath towel around her neck like a cape and declared herself \"Captain Sparklefist,\" ready to save the neighborhood from BOREDOM. ✨\n\n"
            "She ran through the house, \"flying\" with arms out, rescuing her teddy bear from the \"evil couch monster\" and delivering \"justice\" to her brother's messy room. 🧸\n\n"
            "\"Captain Sparklefist, the couch is NOT actually a monster,\" her brother laughed, trying to sound serious.\n\n"
            "\"Every hero needs a villain!\" Rhea declared dramatically, striking a heroic pose on the ottoman.\n\n"
            "By bedtime, the whole family had joined her imaginary adventure, laughing more than they had all week. 😄🦸‍♀️"
        ),
        "think": "🤔 *Think About It!*\nIf YOU were a superhero for a day, what silly, fun name would you give yourself, and what would your superpower be?",
        "moral": "✨ *Today's Lesson:* Imagination can turn an ordinary afternoon into an exciting, joyful adventure."
    },
    {
        "id": 93,
        "category": "Fun",
        "title": "The Sneaky Sock Thief",
        "age": "Ages 5–7 🚀",
        "tradition": "Fun 🎈",
        "text": (
            "🧦 Every week, one single sock would mysteriously vanish from the laundry, leaving lonely, matchless socks behind. \"Where do they GO?\" little Kian wondered.\n\n"
            "He decided to become a detective, setting up a flashlight and a notebook to \"investigate\" the washing machine at midnight. 🔦\n\n"
            "The next morning, he found the culprit: the family dog, Biscuit, had a secret pile of stolen socks hidden behind the sofa, like sleepy trophies! 🐶\n\n"
            "\"Case closed!\" Kian announced proudly, holding up seven mismatched socks.\n\n"
            "The family laughed for days about Biscuit, the sneakiest sock thief in town, and started calling the missing sock pile \"Biscuit's treasure chest.\" 😂"
        ),
        "think": "🤔 *Think About It!*\nHas something in your house ever mysteriously gone missing? Who or what do you think the sneaky culprit might be?",
        "moral": "✨ *Today's Lesson:* Everyday little mysteries can be a fun adventure if you look at them with curiosity instead of frustration."
    },
    {
        "id": 94,
        "category": "Fun",
        "title": "The Invention That Folded Laundry Backwards",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🤖 For the school science fair, ten-year-old Kavya built a laundry-folding machine out of cardboard, string, and an old fan. \"It'll fold clothes perfectly!\" she announced confidently.\n\n"
            "She switched it on — and instead of folding, it flung socks across the gym, sent a shirt flying onto the judge's head, and somehow tied a pair of shorts into a knot shaped like a pretzel! 🥨\n\n"
            "The whole gym erupted into laughter, including the judges.\n\n"
            "Kavya's face turned red — until she noticed everyone was laughing WITH her, not at her, delighted by the chaos.\n\n"
            "She didn't win first prize, but she won the \"Most Entertaining Invention\" award, and spent the rest of the day performing \"the pretzel trick\" on request. 🏆😂"
        ),
        "think": "🤔 *Think About It!*\nHave you ever tried to build or make something that didn't go as planned but turned out funny or interesting anyway?",
        "moral": "✨ *Today's Lesson:* Not every project has to go perfectly to be worth trying — sometimes the mess is the best part."
    },
    {
        "id": 95,
        "category": "Fun",
        "title": "The Day the Principal Wore a Dinosaur Costume",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🦕 Principal Mrs. Fernandes promised that if the whole school read 500 books together for the reading challenge, she'd wear a dinosaur costume for an entire day.\n\n"
            "Nobody believed she'd actually do it — until the school reached 500 books, and the very next Monday, a giant green T-Rex walked into morning assembly, waving with its tiny arms. 😂\n\n"
            "\"RRRAWR!\" Mrs. Fernandes roared into the microphone, tripping slightly over her tail. The entire school screamed with laughter.\n\n"
            "She taught math in the costume, ate lunch in the costume, and even tried (unsuccessfully) to open a door with her tiny dinosaur arms. 🚪\n\n"
            "\"Best. Reading. Challenge. EVER,\" every student agreed, already planning next year's goal."
        ),
        "think": "🤔 *Think About It!*\nWhat silly challenge or reward could motivate you and your friends or family to work toward a big goal together?",
        "moral": "✨ *Today's Lesson:* A shared goal feels more fun and worth the effort when there's a joyful reward waiting at the end."
    },
    {
        "id": 96,
        "category": "Fun",
        "title": "The Great Cafeteria Food Fight (That Wasn't)",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🍕 A tray tipped over in the school cafeteria, and someone shouted \"FOOD FIGHT!\" — but instead of chaos, one clever teacher clapped her hands. \"FREEZE! Whoever moves first loses dessert privileges for a week!\" 🥶\n\n"
            "Two hundred kids froze mid-motion, some holding food halfway to their mouths, others mid-laugh, one boy stuck balancing on one foot. 😂\n\n"
            "The frozen cafeteria looked like the world's funniest photograph — pizza slices hovering, juice boxes tilted, everyone's face stuck in a ridiculous expression.\n\n"
            "After a full, hilarious minute, the teacher finally said, \"Unfreeze — and clean up together!\"\n\n"
            "Everyone burst out laughing and cleaned the mess side by side, and the \"food fight that wasn't\" became the most legendary lunch of the whole year. 🧹😄"
        ),
        "think": "🤔 *Think About It!*\nCan you think of a clever, funny solution that stopped a problem from getting worse — like the teacher's \"freeze\" game?",
        "moral": "✨ *Today's Lesson:* A little creativity and humor can turn a potential mess into a moment everyone remembers fondly."
    },
    {
        "id": 97,
        "category": "Fun",
        "title": "My Homework Turned Into a Talent Show",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🎤 Ten-year-old Neel was supposed to write a boring essay about \"My Summer Vacation,\" but instead, he turned it into a rap, complete with beatboxing sound effects written in the margins. 🎶\n\n"
            "His teacher, expecting a plain essay, read it silently first — then burst out laughing and asked Neel to perform it out loud for the class.\n\n"
            "Neel stood up nervously, then rapped his entire summer vacation story, complete with dramatic pauses and hand gestures. The class cheered and clapped along! 👏\n\n"
            "\"This wasn't exactly the assignment,\" his teacher laughed, \"but it might be the most memorable essay I've ever received.\"\n\n"
            "She gave him full marks — and asked if he'd perform it again at the school's talent show. 🏆"
        ),
        "think": "🤔 *Think About It!*\nIs there a boring task you could make more fun by doing it in a creative or silly way, like turning it into a song or a game?",
        "moral": "✨ *Today's Lesson:* Even ordinary assignments can become fun and memorable with a little creativity."
    },
    {
        "id": 98,
        "category": "Fun",
        "title": "The Class Pet Who Ran for Mayor",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🐹 As a joke during the school's mock election unit, ten-year-old Farida nominated the class hamster, Sir Nibbles, for \"Mayor of the Classroom.\" 🏛️\n\n"
            "\"Vote Nibbles — he never breaks promises, because he never makes any!\" her campaign poster read, complete with a tiny hamster wearing a paper crown.\n\n"
            "To everyone's shock, Sir Nibbles WON, beating out two very serious human candidates with actual speeches.\n\n"
            "\"How did a hamster win a class election?\" the teacher laughed, reviewing the votes.\n\n"
            "\"Because everyone agreed he'd never raise homework taxes,\" Farida said solemnly, and the whole class dissolved into giggles.\n\n"
            "Sir Nibbles \"governed\" for a week, mostly by running on his wheel, and the whole school still talks about the Great Hamster Election. 🎉"
        ),
        "think": "🤔 *Think About It!*\nWhat silly campaign promises would YOU make if you were running for class president — or if your pet was?",
        "moral": "✨ *Today's Lesson:* Learning through play and humor can make even a serious topic, like elections, fun to understand."
    },
    {
        "id": 99,
        "category": "Fun",
        "title": "The Smelliest Science Fair Project",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🧪 For the science fair, ten-year-old Omar decided to grow the \"World's Smelliest Cheese Mold\" as an experiment on bacteria growth. \"For SCIENCE!\" he declared proudly.\n\n"
            "By the third week, his project jar smelled so powerfully bad that three separate teachers asked him to move it to the hallway. 🤢\n\n"
            "On presentation day, judges approached his table, took one whiff, and visibly recoiled, eyes watering. \"This is... certainly memorable,\" one judge coughed.\n\n"
            "Despite — or maybe because of — the smell, Omar's detailed charts on mold growth impressed the judges, and he won \"Most Unforgettable Experiment.\" 🏆\n\n"
            "He proudly kept the ribbon, but agreed the jar could finally, MERCIFULLY, go in the trash. 😂🗑️"
        ),
        "think": "🤔 *Think About It!*\nWhat's the messiest or silliest experiment or project you'd love to try, even if it might go a little wrong?",
        "moral": "✨ *Today's Lesson:* Real science is sometimes messy and stinky — and that's often when the most memorable learning happens."
    },
    {
        "id": 100,
        "category": "Fun",
        "title": "The Time My Family Got Lost Using a GPS That Only Spoke in Riddles",
        "age": "Ages 8–10 📚",
        "tradition": "Fun 🎈",
        "text": (
            "🚗 On a road trip, the family's old GPS app glitched and started giving directions only in riddles. \"Turn where the sun forgets to shine, and greet the road that has no name,\" it announced solemnly. 🧩\n\n"
            "\"What does THAT mean?!\" Dad groaned, squinting at three identical-looking turns.\n\n"
            "Ten-year-old Priya, delighted, grabbed a notebook. \"I'll be the riddle translator!\" She decoded each clue with wild guesses, sending them down one wrong road, then a dead end, then — finally — the right way, purely by luck. 🗺️\n\n"
            "What should have been a twenty-minute drive took two hilarious hours, filled with wrong turns, snack breaks, and Priya's increasingly dramatic riddle theories.\n\n"
            "When they finally arrived, Mom laughed, \"Best. Wrong. Turns. Ever.\" They kept the glitchy GPS app just for fun after that. 😂"
        ),
        "think": "🤔 *Think About It!*\nHas getting lost or taking a 'wrong turn' ever turned into an unexpectedly fun memory for you or your family?",
        "moral": "✨ *Today's Lesson:* Not every unplanned detour is a disaster — sometimes getting lost together is the best part of the trip."
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
