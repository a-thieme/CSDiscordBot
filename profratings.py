import ratemyprofessor as rmp


def prof_rating(name):
    tmp = rmp.get_professor_by_school_and_name(rmp.get_school_by_name('University of Memphis'), name)
    return {'Name': tmp.name, 'Difficulty': tmp.difficulty, 'Rating': tmp.rating, 'Number of Ratings': tmp.num_ratings}


if __name__ == '__main__':
    a = prof_rating('wang')
    print(a)
