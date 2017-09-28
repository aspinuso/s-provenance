var mapFunction = function() {
    var keys = [
        {
            runId: this.runId,
            username: this.username,
            type: 'runId_username'
        },
        {
            username: this.username,
            type: 'username'
        }
    ];
   
    var contentMap = {};
    if (this.streams && Object.prototype.toString.call( this.streams ) === '[object Array]' ) {
        for (let stream of this.streams) {
            if (stream.indexedMeta) {
                for(let indexedMetaItem of stream.indexedMeta) {
                    if (!contentMap[indexedMetaItem.key]) {
                        contentMap[indexedMetaItem.key] = {
                            count: 0,
                            valuesByType: {}
                        }
                    }
                    contentMap[indexedMetaItem.key]['count'] += 1;    

                    const type = typeof indexedMetaItem.val

                    if (type === 'number' && indexedMetaItem.val != NaN && indexedMetaItem.val != Infinity) {
                        if (!contentMap[indexedMetaItem.key]['valuesByType']['number']) {
                            contentMap[indexedMetaItem.key]['valuesByType']['number'] = {
                                count: 1,
                                min: indexedMetaItem.val,
                                max: indexedMetaItem.val 
                            }
                        } else {
                            contentMap[indexedMetaItem.key]['valuesByType']['number']['count'] += 1
                            if (indexedMetaItem.val < contentMap[indexedMetaItem.key]['valuesByType']['number']['min']) {
                               contentMap[indexedMetaItem.key]['valuesByType']['number']['min'] = indexedMetaItem.val 
                            }
                            else if (indexedMetaItem.val > contentMap[indexedMetaItem.key]['valuesByType']['number']['max']) {
                               contentMap[indexedMetaItem.key]['valuesByType']['number']['max'] = indexedMetaItem.val 
                            }
                        }
                    } else if (type === 'string' || type === 'boolean' ) {
                        if (!contentMap[indexedMetaItem.key]['valuesByType'][type]) {
                            contentMap[indexedMetaItem.key]['valuesByType'][type] = {
                                count: 1
                            }
                        } else {
                            contentMap[indexedMetaItem.key]['valuesByType'][type]['count'] += 1
                        } 
                    }

                }
            }
        }
    } 

    var parameterMap = {};
    if (this.parameters && Object.prototype.toString.call( this.parameters ) === '[object Array]' ) {
        for(let parameterItem of this.parameters) {
            if (!parameterMap[parameterItem.key]) {
                parameterMap[parameterItem.key] = {
                    count: 0,
                    valuesByType: {}
                }
            }
            parameterMap[parameterItem.key]['count'] += 1;    

            const type = typeof parameterItem.val

            if (type === 'number' && parameterItem.val != NaN && parameterItem.val != Infinity) {
                if (!parameterMap[parameterItem.key]['valuesByType']['number']) {
                    parameterMap[parameterItem.key]['valuesByType']['number'] = {
                        count: 1,
                        min: parameterItem.val,
                        max: parameterItem.val 
                    }
                } else {
                    parameterMap[parameterItem.key]['valuesByType']['number']['count'] += 1
                    if (parameterItem.val < parameterMap[parameterItem.key]['valuesByType']['number']['min']) {
                       parameterMap[parameterItem.key]['valuesByType']['number']['min'] = parameterItem.val 
                    }
                    else if (parameterItem.val > parameterMap[parameterItem.key]['valuesByType']['number']['max']) {
                       parameterMap[parameterItem.key]['valuesByType']['number']['max'] = parameterItem.val 
                    }
                }
            } else if (type === 'string' || type === 'boolean' ) {
                if (!parameterMap[parameterItem.key]['valuesByType'][type]) {
                    parameterMap[parameterItem.key]['valuesByType'][type] = {
                        count: 1
                    }
                } else {
                    parameterMap[parameterItem.key]['valuesByType'][type]['count'] += 1
                } 
            }
        }
    }         

    for (let key of keys) {
        emit(key, {
            contentMap: contentMap,
            parameterMap: parameterMap
        })
    }
}    

var reduceFunction = function(key, values) {
    var contentMap = {}
    for (let value of values) {
        for (let key in value.contentMap) {
            if (!contentMap[key]) {
                contentMap[key] = value.contentMap[key]
            } else {
                contentMap[key]['count'] += value.contentMap[key]['count']
                for (let type in value.contentMap[key]['valuesByType']) {
                    if (!contentMap[key]['valuesByType'][type]) {
                        contentMap[key]['valuesByType'][type] = value.contentMap[key]['valuesByType'][type]
                    } else {
                        if (type === 'number') {
                            contentMap[key]['valuesByType'][type]['count'] += value.contentMap[key]['valuesByType'][type]['count']
                            if (contentMap[key]['valuesByType'][type]['min'] > value.contentMap[key]['valuesByType'][type]['min']) {
                                contentMap[key]['valuesByType'][type]['min'] = value.contentMap[key]['valuesByType'][type]['min']
                            } else if (contentMap[key]['valuesByType'][type]['max'] < value.contentMap[key]['valuesByType'][type]['max']) {
                                contentMap[key]['valuesByType'][type]['max'] = value.contentMap[key]['valuesByType'][type]['max']
                            }
                        } 
                        // type is string or boolean
                        else {
                            contentMap[key]['valuesByType'][type]['count'] += value.contentMap[key]['valuesByType'][type]['count']
                        }
                    }
                }
            }
        }
    }
    var parameterMap = {}
    for (let value of values) {
        for (let key in value.parameterMap) {
            if (!parameterMap[key]) {
                parameterMap[key] = value.parameterMap[key]
            } else {
                parameterMap[key]['count'] += value.parameterMap[key]['count']
                for (let type in value.parameterMap[key]['valuesByType']) {
                    if (!parameterMap[key]['valuesByType'][type]) {
                        parameterMap[key]['valuesByType'][type] = value.parameterMap[key]['valuesByType'][type]
                    } else {
                        if (type === 'number') {
                            parameterMap[key]['valuesByType'][type]['count'] += value.parameterMap[key]['valuesByType'][type]['count']
                            if (parameterMap[key]['valuesByType'][type]['min'] > value.parameterMap[key]['valuesByType'][type]['min']) {
                                parameterMap[key]['valuesByType'][type]['min'] = value.parameterMap[key]['valuesByType'][type]['min']
                            } else if (parameterMap[key]['valuesByType'][type]['max'] < value.parameterMap[key]['valuesByType'][type]['max']) {
                                parameterMap[key]['valuesByType'][type]['max'] = value.parameterMap[key]['valuesByType'][type]['max']
                            }
                        } 
                        // type is string or boolean
                        else {
                            parameterMap[key]['valuesByType'][type]['count'] += value.parameterMap[key]['valuesByType'][type]['count']
                        }
                    }
                }
            }
        }
    }
    return {
        parameterMap: parameterMap,
        contentMap: contentMap
    }
}


var batch_job = db.getCollection('batch_jobs').findOne({name: 'contentSummary_runId_userName'})

if (!batch_job) {
    db.getCollection('batch_jobs').insert({
        name: 'contentSummary_runId_userName',
        cutoffDateLastJob: new Date("2000-09-28T09:32:38.002Z")
    })
    batch_job = db.getCollection('batch_jobs').findOne({name: 'contentSummary_runId_userName'})
}


var startOfJobString = new Date().toISOString()
var cutoffLastJobString = batch_job.cutoffDateLastJob.toISOString();

var batch_job = true
if (batch_job) {
    db.lineage.mapReduce(
        mapFunction,
        reduceFunction,
        {
            query: {
                "startTime": {
                    '$gte': cutoffLastJobString,
                    '$lte': startOfJobString
                }
            },
            out: { 
                reduce: "term_summaries" 
            },
            sort: {
                runId: 1
            },
            jsMode: true
        }
    )
    db.getCollection('batch_jobs').update({name: 'contentSummary_runId_userName'},{$set: {cutoffDateLastJob: new Date(startOfJobString)}})

} else {
    print('Job not found')
}