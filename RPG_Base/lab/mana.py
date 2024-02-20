    def advance(self, pos, rot, amt):
        pos[0] += math.cos(rot) * amt
        pos[1] += math.sin(rot) * amt
        return pos

    def render_mana(self, size=[4, 6]):
        self.points = []
        self.surf = mana_surf(self.rect)

        for i in range(8):
            self.points.append(self.advance([20,20], self.t / 30 + i / 8 * math.pi * 2, (math.sin((self.t * math.sqrt(i)) / 20) * size[0] + size[1])))
        
        pygame.draw.polygon(self.surf, self.color1, self.points)
        pygame.draw.polygon(self.surf, self.color2, self.points, 1)

        self.surf = pygame.transform.scale_by(self.surf, 3)