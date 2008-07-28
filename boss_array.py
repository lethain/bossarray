from yos.boss import ysearch
from yos.yql import db

class BossArray(object):

    def __init__(self, term):
        self.term = term
        self.retrieved = []
        self.length = None

    def _cache(self, start, results,sort=True):
        i = start
        for result in results:
            self.retrieved.append((i,result))
            i = i + 1
        if sort is True:
            self.retrieved.sort()

    def _cached_portion(self, start, count):
        def contains_result(n):
            for pos,val in self.retrieved:
                if pos == n:
                    return val
            return None
        cached = []
        not_cached = []
        for i in xrange(start,start+count):
            val = contains_result(i)
            if val is not None:
                cached.append((i,val))
            else:
                not_cached.append(i)
        return cached,not_cached

    def _download(self, start, count, sort=True):
        rows = []
        length = 0
        for i in xrange(0, count, 50):
            offset = i * 50
            pos = start + offset
            num_results = min(count - offset, 50)
            data = ysearch.search(self.term,start=pos,count=num_results)
            length = data['ysearchresponse']['totalhits']
            rows = rows + db.create(data=data).rows

        self.length = int(length)
        self._cache(start,rows,sort=sort)
        return rows

    def __getitem__(self, i):
        if type(i) == int:
            cached, not_cached = self._cached_portion(i,0)
            if cached == []:
                return self._download(i,1)[0]
            else:
                return cached[0][1] # [(index,value),]
        else:
            cached, not_cached = self._cached_portion(i.start,i.stop-i.start)
            length = len(not_cached)
            if length == 0:
                return tuple(x[1] for x in cached)
            elif length == 1:
                index = not_cached[0]
                downloaded = [(index,self._download(index,1),)]
            else:
                runs = []
                length = len(not_cached)
                start_of_run = not_cached[0]
                prev = start_of_run
                for i in xrange(1,length):
                    val = not_cached[i]
                    if val - prev == 1:
                        if i != length-1:
                            pass
                        else:
                            runs.append((start_of_run,1+val-start_of_run))
                    else:
                        runs.append((start_of_run,val-1-start_of_run))
                        if i < length - 1:
                            start_of_run = not_cached[i]
                    prev = val
                for index,count in runs:
                    print run
                        
            cached.append(downloaded)
            cached.sort()
            return tuple(x[1] for x in cached)

    def __len__(self):
        if self.length is None:
            self._download(0,1)
        return self.length
            
            
