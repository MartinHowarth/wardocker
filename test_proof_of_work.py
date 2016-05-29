from proof_of_work import manager, worker

man = manager.WorkManager(1000000)

work = worker.Worker(man)

for i in range(10):
    work.request_work()
    work.do_work()
    print(work.guess, work.nonce, work._last_work_time)
    work.submit_work()
