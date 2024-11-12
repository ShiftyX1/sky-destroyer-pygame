class CollisionManager:
    def check_collision(self, obj1, obj2):
        """
        Проверка столкновения между двумя объектами
        используя их границы (rect)
        """
        return (obj1.right > obj2.x and 
                obj1.x < obj2.right and
                obj1.top > obj2.y and
                obj1.y < obj2.top)
    
    def check_boundary(self, obj, left, right, top, bottom):
        """
        Проверка выхода объекта за границы
        """
        return (obj.x < left or 
                obj.right > right or
                obj.y < bottom or
                obj.top > top)