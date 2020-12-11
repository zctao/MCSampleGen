def getAfterFSR(particle, particleCollection):
    PID = particle.PID
    result = particle
    isLast = True

    while result.Status != 1:
        isLast = True
        # loop over all daughters
        for index in range(result.D1, result.D2+1):
            if index < 0:
                continue
            daughter = particleCollection[index]
            DaugPID = daughter.PID
            if DaugPID == PID:
                result = daughter
                isLast = False
                break
        if isLast:
            break

    return result

def getBeforeFSR(particle, particleCollection):
    # TODO
    return particle

def getGenParticle(pdgId, particleCollection, afterFSR=True):
    for particle in particleCollection:
        if particle.PID != pdgId:
            continue

        if afterFSR:
            return getAfterFSR(particle, particleCollection)
        else:
            return getBeforeFSR(particle, particleCollection)

def getTopAfterFSR(particleCollection):
    return getGenParticle(6, particleCollection, afterFSR=True)

def getAntiTopAfterFSR(particleCollection):
    return getGenParticle(-6, particleCollection, afterFSR=True)

def isHadronicTop(top, particleCollection):
    assert(abs(top.PID)==6)

    # get the W boson from top decay
    Wboson = None

    for index in range(top.D1, top.D2+1):
        if index < 0:
            continue

        daughter = particleCollection[index]

        if abs(daughter.PID) == 6:
            # get the top after FSR i.e. the last top
            tlast = getAfterFSR(top, particleCollection)
            return isHadronicTop(top, particleCollection)
        elif abs(daughter.PID) == 24:
            Wboson = daughter
            break

    assert(Wboson is not None)
    Wlast = getAfterFSR(Wboson, particleCollection)

    # get the first daughter of W
    Wdaughter = particleCollection[Wlast.D1]

    if abs(Wdaughter.PID) >= 11 and abs(Wdaughter.PID) <=14:
        return False
    elif abs(Wdaughter.PID)==15 or abs(Wdaughter.PID)==16:
        # W -> tau + nu_tau
        return False # TODO: differentiate leptonic and hadronic tau decay?
    else:
        return True
