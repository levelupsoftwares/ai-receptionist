INTENTS = {
    "booking":   ["book","booking","schedule","appointment","reserve","come","visit","send someone","technician","repair","fix","inspection","check","available","availability","today","tomorrow","this week","as soon as possible","now","asap","am","pm",],
    "emergency": ["emergency","urgent","immediately","right now","burst","pipe burst","flood","flooding","overflow","overflowing","water everywhere","major leak","leaking badly","severe leak","toilet overflowing","can't stop water",],
    "farewell":  ["bye","goodbye","thanks","thank you","that's all","that is all","nothing else","see you","talk later","have a good day",],
    "listening":["uh huh","uh-huh","huh","hmm","hmmm","mm","mmm","mmhmm","mhmm","ah","oh","ooh","wow","right right","i see","see","gotcha","roger","copy that","ok","yeah"],
    "general":   []  # default fallback
}

def detect_intent(text:str)->str:
    text = text.lower()
    for intent,keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                return intent
    return 'general'


# print(detect_intent('hmm'))