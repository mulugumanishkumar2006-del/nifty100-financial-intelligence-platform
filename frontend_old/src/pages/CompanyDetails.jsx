import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Layout from "../components/Layout";

import CompanyHeader from "../components/company/CompanyHeader";
import CompanySummary from "../components/company/CompanySummary";

import HealthScore from "../components/company/HealthScore";
import GrowthAnalysis from "../components/company/GrowthAnalysis";
import RiskAnalysis from "../components/company/RiskAnalysis";

import ProfitLossTable from "../components/company/ProfitLossTable";
import BalanceSheetTable from "../components/company/BalanceSheetTable";
import CashFlowTable from "../components/company/CashFlowTable";
import FinancialRatios from "../components/company/FinancialRatios";

import RevenueChart from "../components/company/RevenueChart";
import ProfitChart from "../components/company/ProfitChart";

import PeerComparison from "../components/company/PeerComparison";

import { getCompany } from "../services/companyService";



function CompanyDetails(){

    const { id } = useParams();


    const [company,setCompany] = useState(null);

    const [loading,setLoading] = useState(true);



    useEffect(()=>{


        async function fetchCompany(){


            try{


                const response = await getCompany(id);


                console.log(
                    "API RESPONSE:",
                    response
                );


                setCompany(response);



            }
            catch(error){


                console.error(
                    "API ERROR:",
                    error
                );


            }
            finally{


                setLoading(false);


            }


        }



        fetchCompany();



    },[id]);





    if(loading){


        return(

            <Layout>

                <h2>
                    Loading Company...
                </h2>

            </Layout>

        );

    }





    if(!company){


        return(

            <Layout>

                <h2>
                    Company Not Found
                </h2>

            </Layout>

        );

    }





    return(


        <Layout>



            {/* ===============================
                Company Header
            =============================== */}


            <CompanyHeader

                company={
                    company.company
                }

            />






            {/* ===============================
                Company Summary
            =============================== */}


            <CompanySummary

                company={
                    company.company
                }

            />







            {/* ===============================
                Financial Intelligence
            =============================== */}



            <HealthScore

                company={
                    company.company
                }

            />



            <GrowthAnalysis

                company={
                    company
                }

            />



            <RiskAnalysis

                company={
                    company
                }

            />







            {/* ===============================
                Charts
            =============================== */}



            <RevenueChart

                company={
                    company
                }

            />



            <ProfitChart

                company={
                    company
                }

            />







            {/* ===============================
                Financial Statements
            =============================== */}



            <ProfitLossTable

                data={
                    company.profit_loss || []
                }

            />



            <BalanceSheetTable

                data={
                    company.balance_sheet || []
                }

            />



            <CashFlowTable

                data={
                    company.cash_flow || []
                }

            />








            {/* ===============================
                Financial Ratios
            =============================== */}



            <FinancialRatios

                company={
                    company.company
                }

            />







            {/* ===============================
                Peer Comparison
            =============================== */}



            <PeerComparison

                company={
                    company.company
                }

            />



        </Layout>


    );

}



export default CompanyDetails;