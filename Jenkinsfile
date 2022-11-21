defaultBranch = env.BRANCH_NAME.replace("/","%2F")

pipeline {

  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '15', artifactNumToKeepstr: '5'))
  }

  parameters {
    booleanParam(name: 'doClean', defaultValue: true, description 'Clean the project workspace before build')
  }

  stages {

    stage("Clean") {
      when {
        expression {
          params.doClean
        }
      }
      steps {
        cleanWs()
      }
    }

    stage("Git Checkout") {
      steps {
        checkout scm
      }
    }

    stage("SetUp") {
      script {
        if (env.GIT_BRANCH == 'develop' || env.GIT_BRANCH ==~ /(.+)feature-(.+)/) {
          target    = 'dev'
          BuildType = '-dev'
        } else if ( env.GIT_BRANCH ==~ /(.+)release-(.+)/) {
          target    = 'pre'
          BuildType = '-RC'
        } else if ( env.GIT_BRANCH == 'master' || env.GIT_BRANCH == 'main' ) {
          target    = 'prod'
          BuildType = ''
        } else {
          error "Unknown branch type: ${env.GOT_BRANCH}. Expected one of (develop/feature-/release-/master/main)"
        }

        oversion = sh(script: "./scorch -v | cut -d '[' -f2 | tr -d ']'", returnStout: true).trim()

        version     = oversion.take(10) + "-" + env.BUILD_NUMBER
        oversion    = oversion.take(10)
        iacname     = env.JOB_NAME

        prjname     = 'scorch'

        packagename = iacname + '-v' + version + 'tar.gz'

        publish_url = env.NEXUS_URL + '/repository/' + prjname + '/' + package
      }
      
    stage('Build') {
      steps {
        script {
          tagversion = sh(script: "git -c 'versionsort.suffix=-' \
                                   ls-remote --exit-code --refs --sort='version:refname' --tags \
                                   | tail --lines=1 \
                                   | cut --delimiter="/" --fields=3", returnStdout: true).trim() + BuildType
        }
        echo "INFO: Latest Tag: " + tagversion
        echo "INFO: Building $prjname from $target branch"
        echo "INFO: Build number: $BUILD_NUMBER"
        echo "INFO: Job name: ${env.JOB_NAME}"
        echo "INFO: Publish URL: " + publish_url

        sh "mkdir -p ${prjname}-${BUILD_NUMBER}"
        sh "sed -i s/^BUILDTAG=.*/BUILDTAG=${tagversion}/ scorch"
        sh "mkdir -p plugins ; chmod 775 plugins"
        sh "ls -l"
        sh "tar cf ${prjname}-${tagversion}.tar LICENSE README.md scorch obrar bin python functions plugins projects/common"
        sh "sha256sum ${prjname}-${tagversion}.tar > ${prjname}-${tagversion}.tar.sha256"
        sh "md5sum    ${prjname}-${tagversion}.tar > ${prjname}-${tagversion}.tar.md5"
      }   
    }

    stage("CI UNIT Test") {
      when {
        expression { target == 'dev' }
      }
      steps {
        echo "Extracting and checking...."
        sh "ls -l ${prjname}-${targetversion}.tar"
        dir('${prjname}-${BUILD_NUMBER}') {
          sh "tar xf ../${prjname}-${targetversion}.tar"
          sh "./scorch -h"
          sh "./scorch -v"
        }
      }
    }

    stage('Approval') {
      when {
        expression {target = 'prod'}
      }
      steps {
        timeout(time:30, unit:'MINUTES') {
          input message: "Deploy to Production?", id: 'approval'
        }
      }
    }
    
  }

  post {
    always {
      sh "df -h"
      archiveArtifacts artifacts: '*.tar, *.sha256, *.md5', followSymlinks: false
    }
  }
}




// node {
//   checkout scm

//   stage 'test'
//   sh 'echo test'

//   stage 'package'
//   sh 'tar cf scorch.tar LICENSE README.md scorch obrar bin python functions plugins/DEMO'

// //   /var/apache-maven/bin/mvn clean package
// //  str_ProgramName=scorch
// //  if $SNAPSHOT ; then
// //    str_ProgramVersion=$RELEASE
// //  else
// //    str_ProgramVersion=$(grep -a "^typeset str_ProgramVersion=" ${str_ProgramName} | cut -d"=" -f2 | tr -d '"')
// //  fi

// //  ls -lR
// //  tar cf scorch.tar ${str_ProgramName} bin obrar python functions plugins/DEMO

// //  md5sum scorch.tar > scorch.tar.md5
// //  cp scorch.tar      escorch.${str_ProgramVersion}.tar
// //  cp scorch.tar.md5  escorch.${str_ProgramVersion}.tar.md5.txt
// //  echo ${str_ProgramVersion} > version.txt

// //  mv scorch.tar      latest.tar
// //  mv scorch.tar.md5  latest.tar.md5
// //  mv bin/install     install

//   stage 'publish'
//   sh 'echo publish'
// }
