class ProcessorBase:
    def anonymize(self, inp, out, manager, detector) -> None:
        raise NotImplementedError

    def restore(self, inp, out, manager) -> None:
        raise NotImplementedError
