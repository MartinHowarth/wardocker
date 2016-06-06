from proof_of_work import manager, worker

man = manager.WorkManager(1000000)

work = worker.Worker(man)

for i in range(10):
    work.create_work_request()
    work.do_work()
    print(work.guess, work.nonce, work._last_work_time)
    work.create_work_submission()
