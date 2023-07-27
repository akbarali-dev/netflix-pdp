from django.test import TestCase, Client
from datetime import date

from movies.models import Actor, Movie


class TestMovieViewSet(TestCase):
    def setUp(self) -> None:
        self.actor1 = Actor.objects.create(name="Test Actor 1", birth_date=date(1949, 1, 1))
        self.actor2 = Actor.objects.create(name="Test Actor 2", birth_date=date(1949, 1, 1))

        self.movie2 = Movie.objects.create(year=date(1949, 1, 1), name="Charlie Chaplin", imdb=8, genre="comedy")
        self.movie2.actors.add(self.actor1.id)

        self.movie1 = Movie.objects.create(year=date(1949, 1, 1), name="titanic", imdb=6, genre="drama")
        self.movie1.actors.add(self.actor1.id)
        self.movie1.actors.add(self.actor2.id)

        self.movie3 = Movie.objects.create(year=date(1949, 1, 1), name="Mr Bin", imdb=9, genre="comedy")
        self.movie3.actors.add(self.actor2.id)

        self.movie4 = Movie.objects.create(year=date(1949, 1, 1), name="Test", imdb=1, genre="comedy")
        self.movie4.actors.add(self.actor2.id)

        self.client = Client()

    def test_get_all_movie(self):
        response = self.client.get("/movies/")
        data = response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 4)
        self.assertIsNotNone(data[0]['id'])
        self.assertEquals(data[0]['name'], 'Charlie Chaplin')

    def test_search(self):
        response = self.client.get("/movies/?search=titanic")
        data = response.data
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(data), 1)
        self.assertIsNotNone(data[0]['id'])
        self.assertEquals(data[0]['name'], 'titanic')

    def test_orderid_asc(self):
        response = self.client.get("/movies/?ordering=imdb")
        data = response.data
        check_order = self.check_ordered(data, True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(data[0]['imdb'], 1)
        self.assertTrue(check_order)

    def test_orderid_desk(self):
        response = self.client.get("/movies/?ordering=-imdb")
        data = response.data
        check_order = self.check_ordered(data, False)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(data[0]['imdb'], 9)
        self.assertTrue(check_order)

    @staticmethod
    def check_ordered(data, is_ascending):
        check_order = True
        start = 0
        stop = len(data) - 1
        step = 1
        if not is_ascending:
            start = len(data)-1
            stop = 0
            step = -1

        for i in range(start, stop, step):
            if data[i]['imdb'] <= data[i + step]['imdb']:
                check_order = True
            else:
                return False
        return check_order
