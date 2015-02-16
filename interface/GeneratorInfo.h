#pragma once

#include <Rtypes.h>


namespace pec
{
    /**
     * \class GeneratorInfo
     * \author Andrey Popov
     * \brief Aggregates basic generator-level information
     */
    class GeneratorInfo
    {
    public:
        /// Constructor without parameters
        GeneratorInfo();
        
        /// Copy constructor
        GeneratorInfo(GeneratorInfo const &src);
        
        /// Assignment operator
        GeneratorInfo &operator=(GeneratorInfo const &src);
        
    public:
        /// Resets the object to a state right after the default initialisation
        void Reset();
        
        /**
         * \brief Sets process ID
         * 
         * See documentation for the method ProcessID for details.
         */
        void SetProcessId(int processID);
        
        /// Sets generator-level event weight
        void SetWeight(double weight);
        
        /**
         * \brief Sets momentum fraction carried by an initial parton
         * 
         * Throws an exception if the given index is large than or the fraction is illegal.
         */
        void SetPdfX(unsigned index, double x);
        
        /**
         * \brief Sets momentum fractions for both initial partons simultaneously
         * 
         * Internally, calls to SetPdfX, check documentation for this method.
         */
        void SetPdfXs(double x1, double x2);
        
        /**
         * \brief Sets ID of an initial parton
         * 
         * Gluons must be encoded with zeros instead of code 21. If the index is larger than 1, an
         * exception is thrown.
         */
        void SetPdfId(unsigned index, int id);
        
        /**
         * \brief Sets IDs of both initial partons
         * 
         * Internally, calls to SetPdfId, check documentation for this method.
         */
        void SetPdfIds(int id1, int id2);
        
        /// Sets energy scale used to evaluate PDF, GeV
        void SetPdfQScale(double scale);
        
        /**
         * \brief Returns process ID
         * 
         * This is supposed to be the process ID set be the generator. For instance, different
         * subprocesses in MadGraph are assigned different process IDs.
         */
        int ProcessId() const;
        
        /**
         * \brief Returns generator-level event weight
         * 
         * Note that the weight might be negative for some generators, e.g. in aMC@NLO.
         */
        double Weight() const;
        
        /**
         * \brief Returns momentum fraction carried by an initial parton
         * 
         * Throws an exception if the index is larger than 1.
         */
        double PdfX(unsigned index) const;
        
        /**
         * \brief Returns ID of an initial parton
         * 
         * Gluons are encoded by zeros. If the index is larger than 1, an exception is thrown.
         */
        int PdfId(unsigned index) const;
        
        /// Returns energy scale used to evaluate PDF, GeV
        double PdfQScale() const;
        
    private:
        /// Process ID as was set during generation of the sample
        Short_t processId;
        
        /**
         * \brief Generator-level weight
         * 
         * Encoded as a generic minifloat with parameters (true, 10, 14), the range representable
         * with normal numbers is [6.1e-5, 1.3e5s).
         */
        UShort_t weight;
        
        /**
         * \brief Momenta fractions carried by initial-state partons
         * 
         * Encoded as a generic minifloat with parameters (false, 13, 7), the range representable
         * with normal numbers is [7.8e-3, 1).
         */
        UShort_t pdfX[2];
        
        /**
         * \brief ID of initial-state partons
         * 
         * The two are encoded in a single byte. First ID is (pdfID % 16 - 5), the second is
         * (pdf / 16 - 5). Gluons are encoded with zeros.
         */
        UChar_t pdfId;
        
        /**
         * \brief Energy scale to evaluate PDF, GeV
         * 
         * Encoded as a generic minifloat with parameters (false, 12, 0), the range representable
         * with normal numbers is [1, 32k).
         */
        UShort_t pdfQScale;
    };
}