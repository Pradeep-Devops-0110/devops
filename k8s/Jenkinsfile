pipeline {
  agent any

  environment {
    REGISTRY = 'rvp0110/micro-dev'
    IMAGE_TAG = 'latest'
  }
    stage('Build Images') {
      steps {
        sh """
          docker build -t ${REGISTRY}/catalog-service:${IMAGE_TAG} ./catalog-service
          docker build -t ${REGISTRY}/order-service:${IMAGE_TAG} ./order-service
          docker build -t ${REGISTRY}/payment-service:${IMAGE_TAG} ./payment-service
        """
      }
    }

    stage('Push Images') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh """
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker push ${REGISTRY}/catalog-service:${IMAGE_TAG}
            docker push ${REGISTRY}/order-service:${IMAGE_TAG}
            docker push ${REGISTRY}/payment-service:${IMAGE_TAG}
          """
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_FILE')]) {
          sh """
            export KUBECONFIG=${KUBECONFIG_FILE}
            kubectl apply -f k8s/
            kubectl rollout status deployment/catalog-deployment --timeout=120s || true
            kubectl rollout status deployment/order-deployment --timeout=120s || true
            kubectl rollout status deployment/payment-deployment --timeout=120s || true
          """
        }
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}
