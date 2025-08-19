import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex items-center justify-between py-20">
        <div className="flex-1 max-w-xl">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Your AI-powered Health Companion
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Get instant insights about your symptoms with our advanced AI technology. 
            Quick, reliable, and always available when you need it most.
          </p>
          <Link
            to="/symptom-checker"
            className="inline-block bg-primary text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            Check Symptoms Now
          </Link>
        </div>
        <div className="flex-1 ml-12">
          <div className="bg-gradient-to-br from-blue-100 to-blue-200 rounded-2xl p-8 shadow-xl">
            <div className="text-center">
              <div className="text-6xl mb-4">🏥</div>
              <h3 className="text-2xl font-semibold text-gray-800 mb-2">Healthcare AI</h3>
              <p className="text-gray-600">Advanced medical assistance at your fingertips</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home