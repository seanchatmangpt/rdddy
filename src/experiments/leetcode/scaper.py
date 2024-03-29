import dspy
from playwright.sync_api import sync_playwright

from experiments.leetcode.solution_model2 import InterviewCodingChallengeModel
from rdddy.generators.gen_pydantic_instance import GenPydanticInstance
from rdddy.signatures.code_challenge_to_real_world import CodeChallengeToRealWorld
from rdddy.signatures.code_interview_solver import CodeInterviewSolver

leet_list = [
    "/problems/merge-sorted-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/remove-element/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/remove-duplicates-from-sorted-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/remove-duplicates-from-sorted-array-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/majority-element/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/rotate-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/best-time-to-buy-and-sell-stock/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/best-time-to-buy-and-sell-stock-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/jump-game/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/jump-game-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/h-index/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/insert-delete-getrandom-o1/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/product-of-array-except-self/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/gas-station/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/candy/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/trapping-rain-water/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/roman-to-integer/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/integer-to-roman/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/length-of-last-word/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/longest-common-prefix/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/reverse-words-in-a-string/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/zigzag-conversion/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-the-index-of-the-first-occurrence-in-a-string/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/text-justification/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/valid-palindrome/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/is-subsequence/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/two-sum-ii-input-array-is-sorted/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/container-with-most-water/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/3sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-size-subarray-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/longest-substring-without-repeating-characters/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/substring-with-concatenation-of-all-words/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-window-substring/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/valid-sudoku/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/spiral-matrix/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/rotate-image/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/set-matrix-zeroes/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/game-of-life/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/ransom-note/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/isomorphic-strings/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/word-pattern/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/valid-anagram/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/group-anagrams/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/two-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/happy-number/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/contains-duplicate-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/longest-consecutive-sequence/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/summary-ranges/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/merge-intervals/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/insert-interval/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-number-of-arrows-to-burst-balloons/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/valid-parentheses/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/simplify-path/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/min-stack/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/evaluate-reverse-polish-notation/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/basic-calculator/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/linked-list-cycle/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/add-two-numbers/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/merge-two-sorted-lists/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/copy-list-with-random-pointer/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/reverse-linked-list-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/reverse-nodes-in-k-group/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/remove-nth-node-from-end-of-list/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/remove-duplicates-from-sorted-list-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/rotate-list/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/partition-list/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/lru-cache/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/maximum-depth-of-binary-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/same-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/invert-binary-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/symmetric-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/construct-binary-tree-from-preorder-and-inorder-traversal/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/construct-binary-tree-from-inorder-and-postorder-traversal/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/populating-next-right-pointers-in-each-node-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/flatten-binary-tree-to-linked-list/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/path-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/sum-root-to-leaf-numbers/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/binary-tree-maximum-path-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/binary-search-tree-iterator/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/count-complete-tree-nodes/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/lowest-common-ancestor-of-a-binary-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/binary-tree-right-side-view/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/average-of-levels-in-binary-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/binary-tree-level-order-traversal/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/binary-tree-zigzag-level-order-traversal/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-absolute-difference-in-bst/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/kth-smallest-element-in-a-bst/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/validate-binary-search-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/number-of-islands/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/surrounded-regions/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/clone-graph/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/evaluate-division/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/course-schedule/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/course-schedule-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/snakes-and-ladders/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-genetic-mutation/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/word-ladder/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/implement-trie-prefix-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/design-add-and-search-words-data-structure/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/word-search-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/letter-combinations-of-a-phone-number/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/combinations/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/permutations/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/combination-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/n-queens-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/generate-parentheses/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/word-search/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/convert-sorted-array-to-binary-search-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/sort-list/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/construct-quad-tree/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/merge-k-sorted-lists/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/maximum-subarray/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/maximum-sum-circular-subarray/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/search-insert-position/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/search-a-2d-matrix/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-peak-element/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/search-in-rotated-sorted-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-first-and-last-position-of-element-in-sorted-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-minimum-in-rotated-sorted-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/median-of-two-sorted-arrays/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/kth-largest-element-in-an-array/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/ipo/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-k-pairs-with-smallest-sums/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/find-median-from-data-stream/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/add-binary/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/reverse-bits/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/number-of-1-bits/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/single-number/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/single-number-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/bitwise-and-of-numbers-range/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/palindrome-number/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/plus-one/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/factorial-trailing-zeroes/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/sqrtx/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/powx-n/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/max-points-on-a-line/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/climbing-stairs/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/house-robber/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/word-break/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/coin-change/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/longest-increasing-subsequence/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/triangle/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/minimum-path-sum/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/unique-paths-ii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/longest-palindromic-substring/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/interleaving-string/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/edit-distance/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/best-time-to-buy-and-sell-stock-iii/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/best-time-to-buy-and-sell-stock-iv/editorial/?envType=study-plan-v2&envId=top-interview-150",
    "/problems/maximal-square/editorial/?envType=study-plan-v2&envId=top-interview-150",
]


def main():
    lm = dspy.OpenAI(max_tokens=1000)
    dspy.settings.configure(lm=lm)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        route = leet_list[-1].split("/editorial")[0]
        page.goto(f"https://leetcode.com{route}")

        page.click("button:has-text('Enable Dynamic Layout')")

        page.wait_for_selector('[data-track-load="description_content"]')

        # Select the container element by its attribute
        container = page.query_selector('[data-track-load="description_content"]')

        # Check if the container is found
        if container:
            # Extract text from all child elements within the container
            # This JavaScript snippet will return the text content of all elements, preserving their order
            all_text = page.evaluate(
                """
                (container) => {
                    return Array.from(container.querySelectorAll('*'))
                                 .map(element => element.textContent.trim())
                                 .filter(text => text.length > 0)  // Remove empty strings
                                 .join("\\n");
                }
            """,
                container,
            )

            print("Extracted Text Content:")
            print(all_text)

            challenge = f"```challenge\n{all_text}\n```\nTake all of the code within ```challenge``` and convert to natural language"

            lm = dspy.OpenAI(max_tokens=1000)
            dspy.settings.configure(lm=lm)

            # inst = GenPydanticInstance(root_model=InterviewCodingChallengeModel)(prompt=challenge)

            # print(inst.model_dump())

            print("done")

            cot = (
                dspy.ChainOfThought(CodeChallengeToRealWorld)
                .forward(code_challenge_description=all_text)
                .real_world_scenario
            )
            print(cot)

            cot = (
                dspy.ChainOfThought(CodeInterviewSolver)
                .forward(problem_statement=all_text)
                .detailed_code_solution
            )
            print(cot)
        else:
            print("Container not found.")
        # Close the browser
        browser.close()


if __name__ == "__main__":
    main()
