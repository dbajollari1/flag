class Photo:
    def __init__(self, photoId=0, photoTitle='', photoFileName='', uploadDate=None, uploadBy='', userWebsite = ''): #, photoImg=None
      self.photoId = photoId
      self.photoTitle = photoTitle
      self.photoFileName = photoFileName
      self.uploadDate = uploadDate
      self.uploadBy = uploadBy
      self.userWebsite = userWebsite
      # self.photoImg = photoImg