import unittest
from rpn import eval_rpn, RPNError
import math

class TestRPN(unittest.TestCase):

    def test_basicos(self):
        self.assertEqual(eval_rpn("3 4 +"), 7)
        self.assertEqual(eval_rpn("5 1 2 + 4 * + 3 -"), 14)
        self.assertEqual(eval_rpn("2 3 4 * +"), 14)

    def test_floats(self):
        self.assertAlmostEqual(eval_rpn("2.5 2 *"), 5.0)
        self.assertEqual(eval_rpn("-3 -2 *"), 6)

    def test_div_zero(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 0 /")

    def test_funciones(self):
        self.assertEqual(eval_rpn("9 sqrt"), 3)
        self.assertEqual(eval_rpn("100 log"), 2)
        self.assertAlmostEqual(eval_rpn("1 ln"), 0)
        self.assertAlmostEqual(eval_rpn("1 ex"), math.e)
        self.assertEqual(eval_rpn("2 10x"), 100)
        self.assertEqual(eval_rpn("2 3 yx"), 8)

    def test_inv(self):
        self.assertEqual(eval_rpn("2 1/x"), 0.5)
        with self.assertRaises(RPNError):
            eval_rpn("0 1/x")

    def test_trig(self):
        self.assertAlmostEqual(eval_rpn("90 sin"), 1)
        self.assertAlmostEqual(eval_rpn("0 cos"), 1)
        self.assertAlmostEqual(eval_rpn("1 asin"), 90)

    def test_constantes(self):
        self.assertAlmostEqual(eval_rpn("p"), math.pi)
        self.assertAlmostEqual(eval_rpn("j"), (1 + 5**0.5)/2)

    def test_pila(self):
        self.assertEqual(eval_rpn("3 dup *"), 9)
        self.assertEqual(eval_rpn("3 4 swap -"), 1)
        self.assertEqual(eval_rpn("3 4 drop"), 3)

    def test_clear_error(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 4 clear")

    def test_memoria(self):
        self.assertEqual(eval_rpn("5 sto 0 rcl 0"), 5)

    def test_memoria_error(self):
        with self.assertRaises(RPNError):
            eval_rpn("5 sto 10")

        with self.assertRaises(RPNError):
            eval_rpn("5 sto")

    def test_token_invalido(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 4 foo")

    def test_pila_insuficiente(self):
        with self.assertRaises(RPNError):
            eval_rpn("+")

    def test_pila_final(self):
        with self.assertRaises(RPNError):
            eval_rpn("3 4")

    def test_chs(self):
        self.assertEqual(eval_rpn("5 chs"), -5)

    def test_trig_extra(self):
        self.assertAlmostEqual(eval_rpn("1 acos"), 0)
        self.assertAlmostEqual(eval_rpn("1 atg"), 45)

    def test_const_e(self):
        import math
        self.assertAlmostEqual(eval_rpn("e"), math.e)

    def test_clear_ok(self):
        self.assertEqual(eval_rpn("3 4 clear 5"), 5)

    def test_sqrt_error(self):
        with self.assertRaises(ValueError):
            eval_rpn("-1 sqrt")

    def test_log_error(self):
        with self.assertRaises(ValueError):
            eval_rpn("-1 log")

    def test_ln_error(self):
        with self.assertRaises(ValueError):
            eval_rpn("-1 ln")


if __name__ == "__main__":
    unittest.main()