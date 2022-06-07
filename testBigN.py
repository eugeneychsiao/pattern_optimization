import random


class Test:
    def __init__(self):
        self.a = 0
        self.b = 500

    def attribute_replace_test(self):
        # For Loop
        for i in range(50000):
            x = self.a
            y = self.a
            z = self.a + self.b

        # While Loop
        i = 0
        while i < 50000:
            i += 1
            x = self.a
            y = self.a
            z = self.a + self.b

        # List Comp
        rand_list = random.sample(range(1, 100000), 50000)
        filtered = [x for x in rand_list if self.a > x if self.b < x]

    def list_comp_test(self):
        oldlist = random.sample(range(1, 100000), 50000)

        # Base List Comp
        newlist = []
        for x in oldlist:
            newlist.append(x * 10)

        # List Comp with If
        newlist = []
        for x in oldlist:
            if x > 100:
                newlist.append(x ** 2)

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
                        newlist.append(x / 2)

    def string_join_test(self):
        sampleText = "Vulputate elementum Interdum erat sociis leo sollicitudin molestie est euismod id. Magnis. " \
                     "Integer lacus curae; porta feugiat lectus. Fusce pede sociis elit Malesuada ultrices libero " \
                     "fusce pulvinar. Hymenaeos class magna scelerisque dapibus tristique primis inceptos turpis, " \
                     "ultricies class eleifend nisl mus penatibus. Dolor orci tristique amet vestibulum praesent " \
                     "nonummy molestie porttitor arcu purus. Lorem rutrum erat natoque inceptos class Primis odio " \
                     "ante eros nec interdum lacus in, hymenaeos praesent ad, mauris fusce lacus vitae posuere mauris " \
                     "sollicitudin quisque augue vehicula. Per ornare. Non tellus, scelerisque dictum, in Gravida " \
                     "ornare semper velit ullamcorper nascetur proin pulvinar pellentesque enim porta. Fringilla " \
                     "pharetra et sit Eget habitasse laoreet aliquam quisque leo. Primis justo cras, et fringilla " \
                     "conubia commodo donec aenean sagittis integer litora. Sed potenti vehicula turpis dapibus " \
                     "euismod felis. Proin aliquet. Torquent sociis litora dignissim curabitur lobortis erat vitae, " \
                     "ante platea pulvinar integer fermentum nunc orci. At orci proin Adipiscing dictum litora. Elit " \
                     "tempus nec aenean sociis nisi. Urna gravida platea lectus. Vulputate lectus consequat Lobortis " \
                     "pulvinar ultricies elementum auctor facilisi, aenean eros platea consequat ullamcorper vehicula " \
                     "non vitae mollis dictum sit sed ornare praesent laoreet cubilia dolor hendrerit ac pharetra " \
                     "suscipit, donec vivamus tristique magna leo penatibus magna eget maecenas bibendum mi vitae, " \
                     "venenatis porttitor sed volutpat. Facilisi interdum senectus nullam consectetuer suspendisse " \
                     "sit nec neque. Aliquet sed sagittis pretium penatibus placerat molestie nulla cum tempus " \
                     "commodo habitasse nullam penatibus cubilia. Cras nulla phasellus molestie. Velit fames tellus " \
                     "nisi duis nunc a, potenti congue enim amet inceptos turpis eget neque sem senectus per " \
                     "porttitor pulvinar. Metus. Pellentesque feugiat. Consequat risus parturient enim. Sodales id " \
                     "lacinia ligula dapibus vehicula condimentum quisque torquent eget semper aptent fringilla " \
                     "pharetra suspendisse nulla curae;. Congue eu quis suscipit eu ac lobortis hymenaeos morbi enim " \
                     "luctus, id diam euismod laoreet primis penatibus fermentum eros enim hac, aliquet nibh " \
                     "tincidunt at sociis proin mauris. Per imperdiet vel ridiculus. Ullamcorper lobortis hac " \
                     "fermentum ipsum. Amet convallis metus Bibendum sollicitudin placerat imperdiet nibh nam " \
                     "lobortis montes phasellus mattis orci sed dignissim erat Convallis pede cum accumsan pede enim " \
                     "curae; ante a, nascetur quisque felis turpis netus vulputate phasellus maecenas faucibus. Id " \
                     "dictumst eu quisque. Pharetra commodo consectetuer ipsum, condimentum egestas est tortor " \
                     "facilisi pede est maecenas conubia in natoque scelerisque senectus pulvinar vel quisque " \
                     "tristique magna quam Praesent natoque proin quis lacus phasellus. Bibendum lobortis. Leo " \
                     "eleifend morbi euismod ipsum. Penatibus Dictum tempor quam diam fermentum venenatis cursus " \
                     "pulvinar in dolor curae; pellentesque phasellus fermentum sagittis eleifend faucibus. Mollis " \
                     "cubilia curabitur quam per augue orci nisi metus tristique congue. Quam eros vehicula. Erat " \
                     "sagittis dapibus at phasellus Maecenas litora tempus nisi. Netus. Dis magna mollis velit " \
                     "feugiat cum, a Ridiculus consectetuer nibh phasellus. Magna mi posuere tristique cum posuere. " \
                     "Volutpat mattis sed nulla. Ad dictum vestibulum congue neque turpis duis hac dictum class. " \
                     "Varius hymenaeos penatibus tristique. Quis aenean sapien lacinia. Hymenaeos arcu integer, " \
                     "ultricies. Nostra erat augue sagittis sapien sit eros habitasse aliquet. Phasellus vulputate, " \
                     "curabitur Vel sed litora laoreet accumsan. Nulla. Gravida, sociosqu pede diam tristique diam " \
                     "ante. Risus netus vitae taciti, amet maecenas habitant dignissim leo non imperdiet. Per " \
                     "fermentum blandit, euismod aliquet nunc. Aptent conubia nonummy consequat ante mus natoque. " \
                     "Mollis elementum purus aliquam elementum suspendisse et urna. Ac. Curae; pellentesque justo " \
                     "ridiculus. Aliquam duis tortor non eleifend sollicitudin mauris. Fusce blandit facilisi, " \
                     "conubia penatibus ultrices. Etiam. Amet. Sem aenean. Sagittis risus sociis maecenas euismod " \
                     "sociosqu odio convallis nunc. Torquent senectus placerat imperdiet nullam pharetra egestas, " \
                     "curae; viverra. Duis sapien volutpat elementum luctus sit in nonummy dolor sed suscipit " \
                     "condimentum dis nisl diam pellentesque aenean condimentum Facilisis iaculis facilisi lectus " \
                     "tempus et. Auctor hymenaeos pretium Sed sodales placerat tortor class tempor. Feugiat. Proin. " \
                     "Donec magnis sagittis euismod lacinia enim feugiat dapibus egestas sem, nostra neque phasellus " \
                     "at massa fusce. Et. Dolor conubia nonummy et. Lacinia a nonummy ornare quisque dictum dis " \
                     "auctor dapibus nisi senectus inceptos leo purus imperdiet ligula tristique donec ante senectus " \
                     "nonummy, odio vitae fringilla urna enim nostra posuere eu dictum commodo ultricies condimentum, " \
                     "cubilia feugiat velit massa. Dignissim mollis a ipsum velit faucibus porta non montes faucibus " \
                     "suspendisse pede mollis lectus interdum parturient natoque ultricies facilisi ridiculus duis " \
                     "lorem. Nunc dignissim tellus sollicitudin nascetur morbi enim neque. Commodo sagittis massa. " \
                     "Libero dictumst aptent vel vestibulum magna dolor penatibus libero commodo nam. Ridiculus " \
                     "montes adipiscing. Facilisi consectetuer. Libero quisque. Nunc mi feugiat vulputate commodo " \
                     "feugiat bibendum quis taciti purus senectus interdum nisi pretium purus nam. Nec cubilia elit " \
                     "enim tortor tortor. Elementum amet. Pede. Mollis orci hac risus felis. Dignissim lorem. " \
                     "Praesent commodo laoreet rutrum aenean dis rutrum elementum egestas placerat mattis suscipit " \
                     "pede. Urna ullamcorper id condimentum congue aliquam morbi, praesent nibh feugiat nam sodales " \
                     "dolor, sollicitudin id vehicula cubilia pellentesque ut hac nostra, pulvinar cras pretium " \
                     "habitant senectus nisl nascetur eros cubilia. Massa ad nunc nonummy Congue vulputate aptent per " \
                     "libero vehicula purus dapibus porta magnis. Magnis dictum diam. Donec iaculis egestas lectus " \
                     "massa tempor cum duis, feugiat aptent. Quis, praesent placerat purus augue elementum. Nullam " \
                     "rhoncus diam leo montes nisl rutrum scelerisque elit ullamcorper massa. Placerat commodo est " \
                     "turpis diam sollicitudin. Placerat hac metus, commodo penatibus penatibus suspendisse odio " \
                     "nascetur convallis platea id. Maecenas taciti netus sagittis mus egestas odio. Ultricies, " \
                     "suspendisse nascetur neque dolor consectetuer. Senectus condimentum. Eu sociosqu fringilla " \
                     "fringilla. Dictum elementum pulvinar integer. Faucibus magnis varius ultrices taciti congue " \
                     "sollicitudin tortor. Vitae urna massa Quam fermentum. Class dis integer vel porttitor vitae " \
                     "Vestibulum lacus nonummy id malesuada enim cursus mauris nec curabitur per nostra duis. Libero " \
                     "laoreet. Vestibulum dui etiam rhoncus. Proin magnis ullamcorper potenti. Primis phasellus " \
                     "facilisi primis. Fringilla molestie nunc pharetra senectus dictumst class nascetur litora " \
                     "pharetra. Elit risus rhoncus. Vehicula, lobortis magnis sociosqu praesent iaculis curae; " \
                     "senectus bibendum sem leo. Facilisi dapibus, quam Enim ad. Urna taciti sapien leo maecenas " \
                     "augue condimentum duis egestas litora class consequat facilisis platea habitasse sodales elit " \
                     "elementum per parturient habitasse ornare felis accumsan eleifend Primis elit pretium tristique " \
                     "ante lacinia pretium ipsum inceptos aptent posuere lacus eleifend nisl congue class Ipsum " \
                     "maecenas. Varius congue nascetur non lobortis egestas. "
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
testClass.attribute_replace_test()
for i in range(50):
    testClass.string_join_test()
