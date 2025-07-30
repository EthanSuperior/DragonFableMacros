from actions import ACT

ACT.Startup()
ACT.LoreBook.Quest()
ACT.MoveInDirection("west")
ACT.Battle("ChaoseWeaver", ("4v", "7"))
