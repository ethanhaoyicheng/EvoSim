import random

class Alias():
    def __init__(self, alias):
        self.alias = alias
    
    def get_alias(self):
        return self.alias

def generate_nickname(entity):
    
    
    titles = titles_index[entity]
    endings = endings_index[entity]

    nickname = ""
    if random.random() < 0.1:
        nickname += titles[random.randint(0,len(titles)-1)]
        nickname += " "
    
    first_type = random.choice([vowel_batch, consonant_batch])
    second_type = vowel_batch if first_type == consonant_batch else consonant_batch
    nickname_length = random.randint(2,3) #up to 5?
    for batch in range(nickname_length):
        if batch == 0 and random.random() < 0.01:
            nickname += "quen"
        else:
            nickname += first_type(batch)
            
            if batch == nickname_length-1 and batch != 0 and random.random() < 0.5:
                last_type = first_type
            else:
                nickname += second_type(batch)
                last_type = second_type

    if random.random() < 0.8:
        nickname += endings[0][random.randint(0,len(endings[0])-1)] if last_type == vowel_batch else endings[1][random.randint(0,len(endings[1])-1)]
    
    nickname_words = nickname.split()
    nickname = " ".join(word[0].upper() + word[1:] for word in nickname_words)
    return Alias(nickname)


def vowel_batch(batch_no):
    vowels = list("aeiou") * 2 + ["oo", "ou", "ui", "ao", "ee", "ei", "y"]
    return random.choice(vowels)

def consonant_batch(batch_no):
    consonants = list("bcdfghjklmnprstvwxz") + ["th"]  #qu
    leaders = list("stgfbkcp")
    followers = list("rlwh") 
    if batch_no >= 1:
        followers.extend("bsnt")

    batch =  random.choice(consonants)
    if batch_no >= 1 and random.random() < 0.2 and len(batch) == 1:
        batch += batch
    elif random.random() < 0.3 and batch[len(batch)-1] in leaders:
        batch += random.choice(followers)

    return batch
        
titles_index = {
    "anima" : ["Mr", "Dr", "Ms", "Mrs", "Lil'", "Big", "Blue", "Tuku"],
    "realm" : ["The Great"]
}

endings_index = {
    "anima" : [[""], [""]],
    "realm" : [["topia", " Island", "'s World", " Land"], [" Island", "'s World", " Land"]]
}

