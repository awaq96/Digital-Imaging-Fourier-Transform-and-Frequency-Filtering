pipeline {
    agent { docker { image 'pmantini/assignment-cosc6380:latest' } }

    environment {
        PATH = "env/bin/:$PATH"
    }
    stages {
        stage('build') {
            steps {
               sh 'python dip_hw3_dft.py > output/dft_output.txt'
                sh 'python dip_hw3_filter.py -i Lenna0.jpg -m ideal_l -c 75'
                sh 'python dip_hw3_filter.py -i Lenna.png -m ideal_h -c 125'
                sh 'python dip_hw3_filter.py -i Lenna0.jpg -m butterworth_l -c 75 -o 2'
                sh 'python dip_hw3_filter.py -i Lenna.png -m butterworth_h -c 125 -o 2'
                sh 'python dip_hw3_filter.py -i Lenna0.jpg -m gaussian_l -c 75'
                sh 'python dip_hw3_filter.py -i Lenna.png -m gaussian_h -c 125'
            }
        }
    }
    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.* ', onlyIfSuccessful: true
        }
    }
}
