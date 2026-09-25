import unittest


class AppSmokeTests(unittest.TestCase):
    def test_imports(self):
        import main
        import qna
        import explanation_module
        import quiz_module
        import summary_module
        import learning_path

        self.assertTrue(hasattr(main, 'app'))
        self.assertTrue(callable(qna.answer_question))
        self.assertTrue(callable(explanation_module.explain_concept))
        self.assertTrue(callable(quiz_module.generate_quiz))
        self.assertTrue(callable(summary_module.summarize_text))
        self.assertTrue(callable(learning_path.get_learning_recommendations))


if __name__ == "__main__":
    unittest.main()
