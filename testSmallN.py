import random


class Test:
    def __init__(self):
        self.a = 0
        self.b = 500

    def attribute_replace_test(self):
        # For Loop
        for i in range(100):
            x = self.a
            y = self.a
            z = self.a + self.b

        # While Loop
        i = 0
        while i < 100:
            i += 1
            x = self.a
            y = self.a
            z = self.a + self.b

        # List Comp
        rand_list = random.sample(range(1, 1000), 100)
        filtered = [x for x in rand_list if self.a > x if self.b < x]

    def list_comp_test(self):
        oldlist = random.sample(range(1, 1000), 100)

        # Base List Comp
        newlist = []
        for x in oldlist:
            newlist.append(x*10)

        # List Comp with If
        newlist = []
        for x in oldlist:
            if x > 100:
                newlist.append(x**2)

        # List Comp with nested If
        newlist = []
        for x in oldlist:
            if x > 50:
                if x < 800:
                    if x < 200:
                        newlist.append(x)

        # List Comp with If Else
        newlist = []
        for x in oldlist:
            if x > 500:
                newlist.append(x)
            elif x < 200:
                newlist.append(x / 2)
            else:
                newlist.append(x / 3)

        # List Comp with nested If Else
        newlist = []
        for x in oldlist:
            if x > 50:
                if x < 800:
                    if x < 200:
                        newlist.append(x)
                    else:
                        newlist.append(x/2)

    def string_join_test(self):
        sampleText = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
        textList = sampleText.split()
        combinedText1 = ""
        combinedText2 = ""
        # augassign .joins
        for i in textList:
            combinedText1 += i

        for i in textList:
            combinedText1 += i + ', '

        for i in textList:
            combinedText1 += '' + i

        # assign .joins
        for i in textList:
            combinedText2 = combinedText2 + i

        for i in textList:
            combinedText2 = combinedText2 + i + ', '


testClass = Test()
testClass.list_comp_test()
testClass.string_join_test()
testClass.attribute_replace_test()
