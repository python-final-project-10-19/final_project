from django.test import TestCase, Client
from .factories import UserFactory
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount
from django.contrib.sites.models import Site

# class TestData(TestCase):

#     @classmethod
#     def setUpTestData(cls):

#         cls.current_site = Site.objects.get_current()

#         cls.SocialApp = cls.current_site.socialapp_set.create(
#             provider="facebook",
#             name="Books Share",
#             client_id="278758722745488",
#             secret="c8a69a48cf6e88181465bf81be8851ce",
#         )


class TestBaseViews(TestCase):
    """Tests for the home page view
    """
    def setUp(self):
        """Test setup
        """
        self.user = UserFactory()
        self.user.save()
        # SocialAccount.objects.create(
        #         provider='facebook',
        #         name='Books Share',
        #         client_id='278758722745488',
        #         secret='c8a69a48cf6e88181465bf81be8851ce',
        #     )
        self.c = Client()

    def test_home_page_without_login(self):
        """If not logged in, user should see login button.
        """
        res = self.c.get('', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Login', res.content)

    def test_home_page_with_login(self):
        """If logged in, user should see logout button.
        """
        self.c.login(
            username=self.user.username,
            password='1qaz@WSX'
        )
        res = self.c.get('account/login/', follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Logout', res.content)


#     def test_view_list_when_logged_in(self):
#         self.c.force_login()

#         budget = BudgetFactory(user=self.user)
#         res = self.c.get('/board/budget')

#         self.assertInHTML(f'<h2>{budget.name}</h2>', res.content.decode())
#         # self.assertIn(budget.name, res.content)

#     def test_lists_only_owned_budgets(self):
#         """test provides login and checks if string is in respose content
#         """
#         self.c.login(
#             username=self.user.username,
#             password='secret'
#         )

#         own_budget = BudgetFactory(user=self.user)
#         other_budget = BudgetFactory()

#         res = self.c.get('/board/budget')
#         # import pdb; pdb.set_trace()
#         self.assertInHTML(f'<h2>{own_budget.name}</h2>', res.content.decode())


#     def test_transactions_listed_in_view(self):
#         self.c.login(
#             username=self.user.username,
#             password='secret'
#         )
#         budget = BudgetFactory(user=self.user)
#         transaction = TransactionFactory(budget=budget)
#         res = self.c.get('/board/budget')

#         self.assertInHTML(str(transaction.amount), res.content.decode())


# class TestTransactionViews(TestCase):
#     pass


# class TestBudgetCreateViews(TestCase):
#     """Class for testing budget view
#     """
#     def setUp(self):
#         self.user = UserFactory()
#         self.user.set_password('super_secret')
#         self.user.save()
#         self.c = Client()

#     def test_new_budget_view(self):
#         self.c.login(
#             username=self.user.username,
#             password='super_secret'
#         )

#         res = self.c.get('/board/budget/new')

#         self.assertEqual(res.status_code, 200)
#         self.assertInHTML('<input type="submit" value="save" />', res.content.decode())


#     def test_create_view_adds_new_budget(self):
#         """tests if user can add new budget data
#         """
#         self.c.login(
#             username=self.user.username,
#             password='super_secret'
#         )

#         form_data = {
#             'name': 'Name thing',
#             'total_budget': 55.5
#         }
#         # import pdb; pdb.set_trace()
#         res = self.c.post(reverse('budget_create_view'), form_data, follow=True)


#         self.assertInHTML('Name thing', res.content.decode())
