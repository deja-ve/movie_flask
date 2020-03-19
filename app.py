# import asyncio
#
#
# async def main():
#     print("hello")
#     await asyncio.sleep(1)
#     print("world")
#
#
# asyncio.run(main())

import asyncio
import time


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


# async def main():
#     print(f"started at {time.strftime('%X')}")
#
#     await say_after(1, 'hello')
#     await say_after(2, 'world')
#
#     print(f"finished at {time.strftime('%X')}")

# async def main():
#     task1 = asyncio.create_task(
#         say_after(1, 'hello'))
#
#     task2 = asyncio.create_task(
#         say_after(2, 'world'))
#
#     print(f"started at {time.strftime('%X')}")
#
#     # Wait until both tasks are completed (should take
#     # around 2 seconds.)
#     await task1
#     await task2
#
#     print(f"finished at {time.strftime('%X')}")
#
#
# asyncio.run(main())

# class Solution:
#     def isRectangleOverlap(self, rec1:list, rec2:list) -> bool:
#         if rec2[0]<rec1[0]:
#             if rec2[2]>rec1[0] and rec2[3]>rec1[1]:
#                 return True
#         elif rec2[0]>=rec1[0] and rec2[0]<rec1[2]:
#             if rec2[1]>rec1[3]:
#                 return False
#             if rec2[3]>rec1[1]:
#                 return True
#
#         else:
#             return False

class Solution:
    def isRectangleOverlap(self, rec1:list, rec2:list) -> bool:
        # if rec2[1] >= rec1[3]:
        #     return False
        # if rec2[3] <= rec1[1]:
        #     return False
        # if rec2[2] <= rec1[0]:
        #     return False
        # if rec2[0] >= rec1[2]:
        #     return False
        if any([rec2[1] >= rec1[3],rec2[3] <= rec1[1],rec2[2] <= rec1[0],rec2[0] >= rec1[2]]):
            return False
        else:
            return True

s = Solution()
print(s.isRectangleOverlap([0,0,1,1],[1,0,2,1]))
